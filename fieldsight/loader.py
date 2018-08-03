import requests
import os
import re
from datetime import datetime

from django.conf import settings
from fieldsight.models import Project
from metadata.models import (
    Gaupalika,
    District,
    Place,
    Ward,
    GeoSite,
    Household,
)


try:
    with open(os.path.join(settings.BASE_DIR, '.env')) as f:
        content = f.read()
except IOError:
    content = ''

for line in content.splitlines():
    m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
    if m1:
        key, val = m1.group(1), m1.group(2)
        m2 = re.match(r"\A'(.*)'\Z", val)
        if m2:
            val = m2.group(1)
        m3 = re.match(r'\A"(.*)"\Z', val)
        if m3:
            val = re.sub(r'\\(.)', r'\1', m3.group(1))
        os.environ.setdefault(key, val)


def get_env(key):
    return os.environ.get(key)


def get_attr(datum, key):
    if key in datum:
        return datum[key]
    if 'attributes' in datum:
        return datum['attributes'].get(key)


class Loader:
    api = '{}/fieldsight/api/remote'.format(get_env('FS_URL'))
    headers = {
        'Authorization': 'Bearer {}'.format(get_env('FS_TOKEN')),
        'Referer': get_env('FS_ORIGIN'),
        'Origin': get_env('FS_ORIGIN'),
    }

    geosite_map = {
        'Category': 'category',
        'Risk_Score': 'risk_score',
        'High_risk_of_': 'high_risk_of',
        'Direct_risk_for': 'direct_risk_for',
        'Potential_impact': 'potential_impact',
        'Risk_Probability': 'risk_probability',
        'Mitigation_work_by': 'mitigation_work_by',
        'Status': 'status',
        'Name_of_place': 'place',
        'Ward': 'ward',
    }

    household_map = {
        'Land_size_allocated_to_HH': 'land_size',
        'Eligibility_Source': 'eligibility_source',
        'Eligibility': 'eligibility',
        'Application': 'application',
        'Result': 'result',
        'Total_Male': 'total_male',
        'Total_Female': 'total_female',
        'Men_Age_0_5': 'men_0_5',
        'Men_Age_6_18': 'men_6_18',
        'Men_Age_19_60': 'men_19_60',
        'Men_Age_60_Plus': 'men_60_plus',
        'Women_Age_0_5': 'women_0_5',
        'Women_Age_6_18': 'women_6_18',
        'Women_Age_19_60': 'women_19_60',
        'Women_Age_60_Plus': 'women_60_plus',
    }

    def fetch_data(self, key):
        url = '{}/{}'.format(self.api, key)
        project, _ = Project.objects.get_or_create(key='key')

        params = {}
        if project.last_updated_at:
            params['last_timestamp'] = project.last_updated_at

        r = requests.get(url, params=params, headers=self.headers)
        response = r.json()

        project.last_updated_at = int(response['timestamp'])
        project.save()

        if not response.get('updated'):
            return []

        return response['data']

    def fetch_geosites(self):
        data = self.fetch_data('geosites')
        for datum in data:
            try:
                self.load_geosite(datum)
            except Exception:
                # TODO Log Error
                pass

    def fetch_households(self):
        data = self.fetch_data('hh_registry')
        for datum in data:
            try:
                self.load_household(datum)
            except Exception:
                # TODO Log Error
                pass

    def load_geosite(self, datum):
        code = get_attr(datum, 'Geohazard_code')
        defaults = {}
        for key, value in self.geosite_map.items():
            defaults[value] = get_attr(datum, key)

        defaults['latitude'] = datum.get('latitude') or \
            datum['location'][1]
        defaults['longitude'] = datum.get('longitude') or \
            datum['location'][0]

        defaults['district'], _ = District.objects.get_or_create(
            name=get_attr(datum, 'District')
        )
        defaults['gaupalika'], _ = Gaupalika.objects.get_or_create(
            name=get_attr(datum, 'Gaupalika'),
            defaults={'district': defaults['district']}
        )
        defaults['place'], _ = Place.objects.get_or_create(
            name=get_attr(datum, 'Name_of_place')
        )
        defaults['ward'], _ = Ward.objects.get_or_create(
            name=get_attr(datum, 'Ward')
        )

        geosite, _ = GeoSite.objects.update_or_create(
            code=code,
            defaults=defaults,
        )

    def load_household(self, datum):
        code = get_attr(datum, 'DS_II_HH_Code')
        geosite = GeoSite.objects.get(code=get_attr(datum, 'Geohazard_Code'))
        if not geosite:
            return

        defaults = {}
        for key, value in self.household_map.items():
            defaults[value] = get_attr(datum, key)

        defaults['geosite'] = geosite
        defaults['district'], _ = District.objects.get_or_create(
            name=get_attr(datum, 'District')
        )
        defaults['gaupalika'], _ = Gaupalika.objects.get_or_create(
            name=get_attr(datum, 'Gaupalika'),
            defaults={'district': defaults['district']}
        )

        household, _ = Household.objects.update_or_create(
            code=code,
            defaults=defaults,
        )

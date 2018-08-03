from django.core.management.base import BaseCommand
from metadata.models import (
    District,
    Gaupalika,
    GeoSite,
)
from utils.geo import get_random_point

import json
import random
import uuid


class Command(BaseCommand):
    num_geo_sites = 2000

    # Choices for fields of geosites
    category = ['CAT1', 'CAT2', 'CAT3']
    risk_score = [
        '625-501',
        '500-401',
        '400-301',
        '300-201',
        '200 - below',
    ]
    high_risk_of = [
        'Major failure', 'Substantial deep-seated failure',
        'Substantial failure', 'Moderate failure',
        'Small failure or erosion',
    ]
    direct_risk_for = [
        'More than 10 households + schools & hospitals',
        '6-10 households',
        '1-5 households',
        'Infrastructure',
        'Agricultural land',
    ]
    potential_impact = [
        'Fatalities',
        'Unrecoverable major damage',
        'Significant damage',
        'Minor damage',
        'Little or no effect',
    ]
    risk_probability = [
        'Almost certain',
        'Very likely',
        'Likely',
        'Possible',
        'Unlikely',
    ]
    mitigation_work_by = [
        'PIN',
        'Government',
        'Name of agency',
        'N/A',
    ]
    status = ['Pending', 'Completed']

    def handle(self, *args, **kwargs):
        self.district = District.objects.all()
        self.gaupalika = Gaupalika.objects.all()

        geo_sites = GeoSite.objects.all()
        i = 0
        for geo_site in geo_sites:
            self.load_geo_site(geo_site)
            i += 1
            print('Geosite #{}'.format(i))

        while i < self.num_geo_sites:
            code = uuid.uuid4().hex[:6].upper()
            geo_site = None
            while not geo_site:
                try:
                    geo_site = GeoSite.objects.create(code=code)
                except Exception:
                    geo_site = None
            self.load_geo_site(geo_site)
            i += 1
            print('Geosite #{}'.format(i))

    def load_geo_site(self, geo_site):
        attrs = [
            'district',
            'gaupalika',
            'category',
            'risk_score',
            'high_risk_of',
            'direct_risk_for',
            'potential_impact',
            'risk_probability',
            'mitigation_work_by',
            'status'
        ]

        for attr in attrs:
            choice = random.choice(getattr(self, attr))
            setattr(geo_site, attr, choice)
        geo_site.place = 'Place {}'.format(uuid.uuid4().hex[:2].upper())

        try:
            gaupalika = geo_site.gaupalika
            pt = get_random_point(json.loads(gaupalika.geojson))
            geo_site.longitude = pt.x
            geo_site.latitude = pt.y
        except Exception:
            pass

        geo_site.save()

from django.core.management.base import BaseCommand
from metadata.models import (
    District,
    Gaupalika,
    GeoSite,
    Household,
)

import random
import uuid


class Command(BaseCommand):
    num_households = 10000

    # Choices for fields of households
    eligibility_source = ['Geohazard', 'Landless']
    eligibility = ['Yes', 'Grievance', 'No']
    application = ['Applied', 'Not applied', 'Declined to apply']
    result = ['Pending', 'Rejected', 'Land certificate', 'Relocated']

    def handle(self, *args, **kwargs):
        self.district = District.objects.all()
        self.gaupalika = Gaupalika.objects.all()
        self.geosite = GeoSite.objects.all()

        households = Household.objects.all()
        i = 0
        for household in households:
            self.load_household(household)
            i += 1
            print('Household #{}'.format(i))

        while i < self.num_households:
            code = uuid.uuid4().hex[:6].upper()
            household = None
            while not household:
                try:
                    household = Household.objects.create(code=code)
                except Exception:
                    household = None
            self.load_household(household)
            i += 1
            print('Household #{}'.format(i))

    def load_household(self, household):
        attrs = [
            'district',
            'gaupalika',
            'geosite',
            'eligibility_source',
            'eligibility',
            'application',
            'result',
        ]

        for attr in attrs:
            choice = random.choice(getattr(self, attr))
            setattr(household, attr, choice)

        household.land_size = random.uniform(1000, 20000)

        attrs = [
            'total_male',
            'total_female',
            'men_0_5',
            'men_6_18',
            'men_19_60',
            'men_60_plus',
            'women_0_5',
            'women_6_18',
            'women_19_60',
            'women_60_plus',
            'other',
        ]

        for attr in attrs:
            choice = random.randint(50, 250)
            setattr(household, attr, choice)
        household.place = 'Place {}'.format(uuid.uuid4().hex[:2].upper())

        household.save()

from django.core.management.base import BaseCommand
from geo.models import Map
from metadata.models import District, Gaupalika

import json


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.load_districts()
        self.load_gaupalikas()

    def load_districts(self):
        map = Map.objects.filter(key='districts').first()
        if not map:
            return

        topojson = json.loads(map.file.read().decode('utf-8'))
        geometries = topojson['objects'][map.default_object]['geometries']
        for geometry in geometries:
            properties = geometry['properties']
            code = properties['district']
            name = properties['district'].capitalize()

            District.objects.update_or_create(
                code=code,
                defaults={'name': name},
            )

    def load_gaupalikas(self):
        map = Map.objects.filter(key='gaupalikas').first()
        if not map:
            return

        topojson = json.loads(map.file.read().decode('utf-8'))
        geometries = topojson['objects'][map.default_object]['geometries']
        for geometry in geometries:
            properties = geometry['properties']
            name = properties['NAME']
            district_name = properties['DISTRICT']

            if not name or not district_name:
                continue

            district = District.objects.filter(name=district_name).first()
            if not district:
                print(
                    'Skipping palika {} because district {} not found'.format(
                        name, district_name
                    )
                )
                continue

            Gaupalika.objects.update_or_create(
                code=name,
                defaults={
                    'name': name,
                    'district': district,
                },
            )

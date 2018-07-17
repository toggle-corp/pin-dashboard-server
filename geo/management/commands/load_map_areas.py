from django.core.management.base import BaseCommand
from geo.models import Map
from metadata.models import District, Gaupalika
import utils.topojson

import json


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Loading districts')
        self.load_districts()
        print('Done')
        print('Loading gaupalikas')
        self.load_gaupalikas()
        print('Done')

    def load_districts(self):
        map = Map.objects.filter(key='districts').first()
        if not map:
            return

        topojson = json.loads(map.file.read().decode('utf-8'))
        scale = topojson['transform']['scale']
        trans = topojson['transform']['translate']
        arcs = topojson['arcs']
        geometries = list(topojson['objects'].values())[0]['geometries']

        for geometry in geometries:
            properties = geometry['properties']
            name = properties['DISTRICT'].capitalize()

            District.objects.update_or_create(
                name=name,
                defaults={
                    'geojson': utils.topojson.geometry(
                        geometry, arcs, scale, trans
                    ),
                },
            )

    def load_gaupalikas(self):
        map = Map.objects.filter(key='gaupalikas').first()
        if not map:
            return

        topojson = json.loads(map.file.read().decode('utf-8'))
        scale = topojson['transform']['scale']
        trans = topojson['transform']['translate']
        arcs = topojson['arcs']
        geometries = list(topojson['objects'].values())[0]['geometries']

        for geometry in geometries:
            properties = geometry['properties']
            name = properties['FIRST_GaPa'].capitalize()
            district_name = properties['FIRST_DIST'].capitalize()

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
                name=name,
                defaults={
                    'district': district,
                    'geojson': json.dumps(utils.topojson.geometry(
                        geometry, arcs, scale, trans
                    )),
                },
            )

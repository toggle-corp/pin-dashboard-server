from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.core.files import File

import os

from geo.models import Map


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        directory = finders.find('sample-maps')
        map_data = [{
            'key': 'districts',
            'filename': 'districts.json',
            'default_object': 'districts',
        }, {
            'key': 'gaupalikas',
            'filename': 'gaupalikas.json',
            'default_object': 'gaupalikas',
        }]

        for info in map_data:
            if Map.objects.filter(key=info['key']).exists():
                continue

            file = open(os.path.join(directory, info['filename']), 'r')
            django_file = File(file)
            map = Map.objects.create(
                key=info['key'],
                default_object=info['default_object'],
            )
            map.file.save(info['filename'], django_file, save=True)

from django.core.management.base import BaseCommand
from fieldsight.loader import Loader


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        loader = Loader()
        loader.fetch_geosites()
        loader.fetch_households()

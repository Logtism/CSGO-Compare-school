from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'setups up stuff'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        call_command('migrate')
        call_command('loaddata', 'catogory', 'subcategory', 'rarity', 'collection', 'container', 'pattern', 'item')
        call_command('runserver')
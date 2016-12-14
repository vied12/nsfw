import django.core.management
from django.core.management.base import BaseCommand

from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Get yesterday reports'

    def handle(self, *args, **options):
        yesterday = (date.today() - timedelta(1)).strftime('%d.%m.%Y')
        countries = ('al', 'ad', 'at', 'by', 'be', 'ba', 'bg', 'hr', 'cy', 'cz', 'dk', 'ee', 'fo', 'fi', 'fr', 'de', 'gi', 'gr', 'hu', 'is', 'ie', 'im', 'it', 'rs', 'lv', 'li', 'lt', 'lu', 'mk', 'mt', 'md', 'mc', 'me', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sm', 'rs', 'sk', 'si', 'es', 'se', 'ch', 'ua', 'gb', 'va', 'rs')
        django.core.management.call_command('eea', date=yesterday, country=countries)

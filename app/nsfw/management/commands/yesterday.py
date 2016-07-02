import django.core.management
from django.core.management.base import BaseCommand

from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Get yesterday reports'

    def handle(self, *args, **options):
        yesterday = (date.today() - timedelta(1)).strftime('%d.%m.%Y')
        django.core.management.call_command('n2o_daily_report', yesterday)
        django.core.management.call_command('pm10_daily_report', yesterday)

from app.nsfw.models import Station, PM10
import requests
import csv
from django.core.management.base import BaseCommand
import datetime


class Command(BaseCommand):
    help = 'Get a PM10 daily report'

    def handle(self, *args, **options):
        req = requests.get('https://www.umweltbundesamt.de/en/luftdaten/stations/\
locations?pollutant=PM1&data_type=1TMW&date=20160629&hour=15')
        content = req.content.decode('utf8')
        for station in list(csv.DictReader(content.splitlines(), delimiter='\t')):
            date = station['date'].split('.')
            date = datetime.date(int(date[2]), int(date[1]), int(date[0]))
            s = Station.objects.get(id=station['stationCode'])
            res = PM10.objects.get_or_create(
                station=s,
                value=station['val'].replace(' µg/m³', ''),
                date=date)
            self.stdout.write(self.style.SUCCESS('%s' % res[0]))

# FIXME: should not save in database, but should create alert

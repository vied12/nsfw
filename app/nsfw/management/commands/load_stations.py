from app.nsfw.models import Station
import requests
import csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update the stations'

    def handle(self, *args, **options):
        req = requests.get('https://www.umweltbundesamt.de/en/luftdaten/stations/\
locations?pollutant=PM1&data_type=1TMW&date=20160629&hour=15')
        content = req.content.decode('utf8')
        for station in list(csv.DictReader(content.splitlines(),
                                           delimiter='\t')):
            res = Station.objects.get_or_create(
                id=station['stationCode'],
                name=station['title'].replace(' %s' % (station['stationCode']),
                                              ''),
                lat=station['lat'],
                lon=station['lon'])
            self.stdout.write(self.style.SUCCESS('%s' % res[0]))

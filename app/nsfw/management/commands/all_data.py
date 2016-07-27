from django.core.management.base import BaseCommand
from app.nsfw.models import Station
import requests


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for station in Station.objects.all():
            if station.id.startswith('DEBE'):
                print(station)
                r = requests.get('https://www.umweltbundesamt.de/en/luftdaten/\
data?pollutant=PM1&data_type=1TMW&date=20130101&\
dateTo={today}&station={station}'.format(today='20160701', station=station.id))
                data = r.content.decode('utf8')
                if data:
                    station.data = data
                    station.save()

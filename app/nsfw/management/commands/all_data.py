from django.core.management.base import BaseCommand
from app.nsfw.models import Station
import requests
import datetime


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--berlin', help='load only berlin data', action='store_const', const=True)

    def handle(self, *args, **kwargs):
        today = datetime.datetime.now().strftime('%Y%m%d')
        for station in Station.objects.all():
            if kwargs['berlin'] and not station.id.startswith('DEBE'):
                continue
            print(station)
            pm10_r = requests.get('https://www.umweltbundesamt.de/en/luftdaten/\
data?pollutant=PM1&data_type=1TMW&date=20130101&\
dateTo={today}&station={station}'.format(today=today, station=station.id))
            no2 = requests.get('https://www.umweltbundesamt.de/en/luftdaten/\
data?pollutant=NO2&data_type=1TMAX&date=20130101&\
dateTo={today}&station={station}'.format(today=today, station=station.id))
            pm10 = pm10_r.content.decode('utf8')
            no2 = no2.content.decode('utf8')
            if pm10 or no2:
                station.pm10_data = pm10
                station.no2_data = no2
                station.save()

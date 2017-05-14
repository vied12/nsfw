from django.core.management.base import BaseCommand
from app.nsfw.models import Station
import requests
import datetime


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--berlin', help='load only berlin data', action='store_const', const=True)

    def handle(self, *args, **kwargs):
        today = datetime.datetime.now().timestamp()
        for station in Station.objects.filter(id__startswith='DE'):
            if kwargs['berlin'] and not station.id.startswith('DEBE'):
                continue
            print(station)
            pm10_r = requests.get('https://www.umweltbundesamt.de/uaq/csv/stations/data?station\
[]={station}&pollutant[]=PM10&scope[]=1TMW&group[]=\
pollutant&range[]=1356998400,{today}'.format(today=today, station=station.id))
            no2 = requests.get('https://www.umweltbundesamt.de/uaq/csv/stations/data?station\
[]={station}&pollutant[]=NO2&scope[]=1SMW_MAX&group[]=\
pollutant&range[]=1356998400,{today}'.format(today=today, station=station.id))
            assert no2.status_code is 200, 'error when downloading data for %s:\n%s' % (station, no2.__dict__)
            assert pm10_r.status_code is 200, 'error when downloading data for %s:\n%s' % (station, pm10_r.__dict__)
            pm10 = pm10_r.content.decode('iso-8859-1')
            no2 = no2.content.decode('iso-8859-1')
            if pm10:
                station.pm10_data = pm10
            if no2:
                station.no2_data = no2
            if pm10 or no2:
                station.save()

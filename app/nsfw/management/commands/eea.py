from app.nsfw.models import Report, Station, Alert, THRESHOLD_PM10, THRESHOLD_NO2
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import datetime
import zipfile
import io
import csv

thresholds = {
    'PM10': THRESHOLD_PM10,
    'NO2': THRESHOLD_NO2,
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='13.12.2015')
        parser.add_argument('--file', help='file to read')
        parser.add_argument('--country', nargs='+', type=str, help='fr')

    def process_report(self, data, date, report=None):
        counter = 0
        stations_by_name = {}
        for station in csv.DictReader(data.splitlines(), delimiter=','):
                # keep only if starting date == date
            if datetime.datetime.strptime(station['value_datetime_begin'][:10], '%Y-%m-%d').date() == date:
                if not stations_by_name.get(station['station_code']):
                    stations_by_name[station['station_code']] = []
                stations_by_name[station['station_code']].append(station)
        for station_name, measures in stations_by_name.items():
            if measures:
                total = sum([float(_['value_numeric']) for _ in measures])
                average = round(total / len(measures))
                stationObj, created = Station.objects.get_or_create(
                    id=station_name,
                    defaults=dict(name=measures[0]['station_name'],
                                  lat=measures[0]['samplingpoint_y'],
                                  lon=measures[0]['samplingpoint_x']))
                if average >= thresholds[measures[0]['pollutant']]:
                    alert, alertCreated = Alert.objects.get_or_create(
                        station=stationObj,
                        report=report,
                        value=average,
                    )
                    counter += 1
        return counter

    def handle(self, *args, **options):
        date = options['date']
        date = list(map(lambda _: int(_), date.split('.')))
        date = datetime.date(date[2], date[1], date[0])
        if options['file']:
            z = zipfile.ZipFile(options['file'])
            csv_content = z.read('AirqualityUTDExport.csv/CSV-output.csv').decode('iso-8859-1')
            self.process_report(csv_content, date)
        else:
            for country in options['country']:
                context = dict(
                    user_token=settings.EEA_TOKEN,
                    country=country,
                    pollutant='PM10',
                    date_from=date.strftime('%Y-%m-%d'),
                    date_to=(date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                )
                url = 'http://fme.discomap.eea.europa.eu/fmedatastreaming/AirQuality/AirQualityUTDExport.fmw?' \
                    'FromDate={date_from}&ToDate={date_to}&Countrycode={country}&InsertedSinceDate=&UpdatedSinceDate=&' \
                    'Pollutant={pollutant}&Namespace=&Format=CSV&UserToken={user_token}'.format(**context)
                self.stdout.write('Fetching %s' % url)
                request = requests.get(url, stream=True)
                try:
                    z = zipfile.ZipFile(io.BytesIO(request.content))
                except:
                    self.stdout.write(self.style.ERROR('%s not a zip' % (country)))
                    continue
                csv_content = z.read('AirqualityUTDExport.csv/CSV-output.csv').decode('iso-8859-1')
                report, created = Report.objects.get_or_create(
                    data=csv_content,
                    country=country,
                    source='eea',
                    kind=context['pollutant'][:3],
                    date=date)
                counter = self.process_report(csv_content, date, report=report)
                if created:
                    self.stdout.write(self.style.SUCCESS('%s: %s' % (country, counter)))

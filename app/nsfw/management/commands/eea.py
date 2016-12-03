from app.nsfw.models import Report
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import datetime
import zipfile
import io


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='13.12.2015')
        parser.add_argument('country', nargs='+', type=str, help='fr')

    def handle(self, *args, **options):
        date = options['date']
        date = list(map(lambda _: int(_), date.split('.')))
        date = datetime.date(date[2], date[1], date[0])
        for country in options['country']:
            context = dict(
                user_token=settings.EEA_TOKEN,
                country=country,
                pollutant='PM10',
                date_from=date.strftime('%Y-%m-%d'),
                date_to=date.strftime('%Y-%m-%d'),
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
            csv_content = z.read('AirqualityUTDExport.csv/CSV-output.csv')
            res, created = Report.objects.get_or_create(
                data=csv_content.decode('iso-8859-1'),
                source='eea',
                kind=context['pollutant'][:3],
                date=date)
            if created:
                self.stdout.write(self.style.SUCCESS('%s %s' % (country, res)))

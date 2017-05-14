from app.nsfw.models import Report
import requests
from django.core.management.base import BaseCommand
import datetime

POLLUTANTS = {
    'PM1': 'PM10',
    'NO2': 'NO2',
}


class UmaCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str, help='13.12.2015')

    def handle(self, *args, **options):
        for date in options['date']:
            date = list(map(lambda _: int(_), date.split('.')))
            date = datetime.datetime(date[2], date[1], date[0])
            date_from = int(date.timestamp())
            date_to = int((date + datetime.timedelta(days=1)).timestamp())
            url = """https://www.umweltbundesamt.de/uaq/csv/stations/data?
station[]=&pollutant[]={pollutant}&scope[]={data_type}&group[]=pollutant&
range[]={date_from},{date_to}""".replace('\n', '').format(
                date_from=date_from,
                date_to=date_to,
                pollutant=POLLUTANTS[self.pollutant],
                data_type=self.data_type)
            print('url', url)
            req = requests.get(url)
            content = req.content.decode('iso-8859-1')
            if content:
                res, created = Report.objects.get_or_create(
                    data=content,
                    country='de',
                    source='uba',
                    kind=self.pollutant,
                    date=date)
                if created:
                    self.stdout.write(self.style.SUCCESS('%s' % res))
            else:
                raise Exception('%s: no data available yet on %s. %s' % (self.pollutant, date, url))

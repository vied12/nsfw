from app.nsfw.models import Report
import requests
from django.core.management.base import BaseCommand
import datetime


class Command(BaseCommand):
    help = 'Get a NO2 daily report'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        for date in options['date']:
            date = list(map(lambda _: int(_), date.split('.')))
            date = datetime.date(date[2], date[1], date[0])
            req = requests.get('https://www.umweltbundesamt.de/en/luftdaten\
/stations/locations?pollutant=NO2&data_type=1TMAX&date={date}\
&hour=15'.format(date=date.strftime('%Y%m%d')))
            content = req.content.decode('utf8')
            res = Report.objects.get_or_create(
                data=content,
                kind='NO2',
                date=date)
            self.stdout.write(self.style.SUCCESS('%s' % res[0]))

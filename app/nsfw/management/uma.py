from app.nsfw.models import Report
import requests
from django.core.management.base import BaseCommand
import datetime


class UmaCommand(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        for date in options['date']:
            date = list(map(lambda _: int(_), date.split('.')))
            date = datetime.date(date[2], date[1], date[0])
            req = requests.get('https://www.umweltbundesamt.de/en/luftdaten\
/stations/locations?pollutant={pollutant}&data_type={data_type}&date={date}\
&hour=15'.format(date=date.strftime('%Y%m%d'),
                 pollutant=self.pollutant,
                 data_type=self.data_type))
            content = req.content.decode('utf8')
            if content:
                res, created = Report.objects.get_or_create(
                    data=content,
                    kind=self.pollutant,
                    date=date)
                if created:
                    self.stdout.write(self.style.SUCCESS('%s' % res))

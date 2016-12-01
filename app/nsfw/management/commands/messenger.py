from django.core.management.base import BaseCommand
from app.nsfw.models import Subscription, Alert, Station
import datetime
from app.messenger_bot.facebook import fb_message
from app.nsfw.models import THRESHOLD_PM10, THRESHOLD_NO2

MAX = {
    'PM10': THRESHOLD_PM10,
    'NO2': THRESHOLD_NO2,
}


class Command(BaseCommand):
    help = 'Send message on Messenger'

    def add_arguments(self, parser):
        parser.add_argument('--test', help='send test message', action='store_const', const=True)

    def handle(self, *args, **options):
        if options['test']:
            self.send_test()
        else:
            self.send_new_alert_to_subscribers()

    def send_test(self):
        to = '1306008742764359'
        alert = Alert.objects.all().first()
        station = Station.objects.all().first()
        self.send_messenger_alert(to, alert, station)
        self.stdout.write(self.style.SUCCESS('test sent'))

    def send_new_alert_to_subscribers(self):
        count = 0
        for sub in Subscription.objects.filter(messenger__isnull=False):
            alerts = Alert.objects.filter(station=sub.station, created__gte=datetime.date.today())
            if alerts:
                alert = alerts[0]
                self.send_messenger_alert(sub.messenger.messenger_id, alert, sub.station)
                count += 1
        self.stdout.write(self.style.SUCCESS('messages sent: %s' % count))

    def send_messenger_alert(self, to, alert, station):
        context = dict(
            value=alert.value,
            kind=alert.report and alert.report.get_kind_display(),
            station=station,
            limit=alert.report and MAX[alert.report.get_kind_display()]
        )
        msgs = [
            '🔴 Pollution alert !',
            'Yesterday we reached {value}µg/m³ of '
            '{kind} pollution at the station {station.name}.\n\n'
            'Based on what has been told by the World Health Organization, we should not be exposed to '
            'more than {limit}µg/m³ of this kind of pollution\n\n',
            'All the data are there:\n'
            'http://smogalarm.org/station/{station.id}'
        ]
        for msg in msgs:
            fb_message(to, msg.format(**context))

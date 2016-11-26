from django.core.management.base import BaseCommand
from app.nsfw.models import Subscription, Alert
import datetime
from app.messenger_bot.views import fb_message


class Command(BaseCommand):
    help = 'Send message on Messenger'

    def handle(self, *args, **options):
        count = 0
        for sub in Subscription.objects.filter(messenger__isnull=False):
            alerts = Alert.objects.filter(station=sub.station, created__gte=datetime.date.today())
            if alerts:
                alert = alerts[0]
                msg = 'Hi !\nYesterday we reached {value}µg/m³ of ' \
                    '{kind} pollution at the station {station}.\n\n' \
                    .format(
                        value=alert.value,
                        kind=alert.report and alert.report.get_kind_display(),
                        station=sub.station
                    )
                fb_message(sub.messenger.messenger_id, msg)
                count += 1
        self.stdout.write(self.style.SUCCESS('messages sent: %s' % count))

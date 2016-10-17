from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from app.nsfw.models import Subscription, Alert
import datetime
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _


class Command(BaseCommand):
    help = 'Send emails'

    def generate_messages(self):
        for sub in Subscription.objects.all():
            alerts = Alert.objects.filter(station=sub.station, created__gte=datetime.date.today())
            if alerts:
                ctx = {'alerts': alerts, 'station': sub.station, 'email': sub.email}
                cur_language = translation.get_language()
                try:
                    translation.activate('de')
                    text = render_to_string('email.txt', ctx)
                finally:
                    translation.activate(cur_language)
                yield (_('Pollution Alerts at %(name)s') % {'name': sub.station.name},  # subject
                       text,  # msg
                       'nsfw@fahrradfreundliches-neukoelln.de',  # from
                       [sub.email.email])  # to

    def handle(self, *args, **options):
        send_mass_mail(self.generate_messages())

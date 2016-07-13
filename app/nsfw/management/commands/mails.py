from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from app.nsfw.models import Subscription, Alert
import datetime
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Send emails'

    def generate_messages(self):
        for sub in Subscription.objects.all():
            alerts = Alert.objects.filter(station=sub.station, created__gte=datetime.date.today())
            if alerts:
                ctx = {'alerts': alerts, 'station': sub.station, 'email': sub.email}
                yield ('Pollution Alerts at %s' % (sub.station.name),  # subject
                       render_to_string('email.txt', ctx),  # msg
                       'nsfw@fahrradfreundliches-neukoelln.de',  # from
                       [sub.email.email])  # to

    def handle(self, *args, **options):
        send_mass_mail(self.generate_messages())

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
import html
from app.messenger_bot.models import Messenger


# From WHO
# see: http://www.who.int/mediacentre/factsheets/fs313/en/
THRESHOLD_PM10 = 50
THRESHOLD_NO2 = 200


class Station(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    pm10_data = models.TextField(null=True, blank=True)
    no2_data = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.id, self.name)


class Report(models.Model):
    KINDS = (('PM1', 'PM10'), ('NO2', 'NO2'))
    data = models.TextField()
    kind = models.CharField(choices=KINDS, max_length=3)
    country = models.CharField(max_length=2)
    date = models.DateField()
    source = models.CharField(max_length=3)

    def __str__(self):
        return '%s (%s)' % (self.get_kind_display(), self.date)

    def process_uba_report(self):
        thresholds = {
            'PM1': THRESHOLD_PM10,
            'NO2': THRESHOLD_NO2,
        }
        for station in list(csv.DictReader(self.data.splitlines(),
                                           delimiter='\t')):
            try:
                val = int(station['val'].replace(' µg/m³', ''))
            except Exception as e:
                print('ERROR', e, station)
                continue
            station, created = Station.objects.get_or_create(
                id=station['stationCode'],
                defaults=dict(name=html.unescape(station['title'].replace(' %s' % (station['stationCode']), '')),
                              lat=station['lat'],
                              lon=station['lon']))
            if val >= thresholds[self.kind]:
                Alert.objects.get_or_create(
                    report=self,
                    station=station,
                    value=val,
                )

    def process_eea_report(self):
        thresholds = {
            'PM1': THRESHOLD_PM10,
            'NO2': THRESHOLD_NO2,
        }
        for station in list(csv.DictReader(self.data.splitlines(),
                                           delimiter=',')):
            try:
                val = round(float(station['value_numeric']))
            except Exception as e:
                print('ERROR', e, station)
                continue
            station, created = Station.objects.get_or_create(
                id=station['station_code'],
                defaults=dict(name=station['station_name'],
                              lat=station['samplingpoint_y'],
                              lon=station['samplingpoint_x']))
            if val >= thresholds[self.kind]:
                Alert.objects.get_or_create(
                    report=self,
                    station=station,
                    value=val,
                )


class Alert(models.Model):
    report = models.ForeignKey('Report', blank=True, null=True)
    station = models.ForeignKey('Station', blank=True, null=True)
    # Date to send alert
    # date = models.DateTimeField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    email = models.ForeignKey('Email', null=True)
    messenger = models.ForeignKey(Messenger, null=True)
    station = models.ForeignKey('Station')

    def __str__(self):
        return '%s\'s subscription to %s' % (self.messenger or self.email.email, self.station)


class Email(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.email


@receiver(post_save, sender=Report)
def on_report_save(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        if instance.source == 'uba':
            instance.process_uba_report()
        # elif instance.source == 'eea':
        #     instance.process_eea_report()

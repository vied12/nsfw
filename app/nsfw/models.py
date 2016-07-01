from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv

THRESHOLD_PM10 = 50


class Station(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return '%s (%s)' % (self.id, self.name)


class Report(models.Model):
    KINDS = (('PM1', 'PM10'), ('NO2', 'NO2'))
    data = models.TextField()
    kind = models.CharField(choices=KINDS, max_length=3)
    date = models.DateField()

    def __str__(self):
        return '%s (%s)' % (self.kind, self.date)

    def process_report(self):
            handlers = {
                'PM1': '_process_pm1_report'
            }
            getattr(self, handlers[self.kind])()

    def _process_pm1_report(self):
        for station in list(csv.DictReader(self.data.splitlines(),
                                           delimiter='\t')):
            val = int(station['val'].replace(' µg/m³', ''))
            station, created = Station.objects.get_or_create(
                id=station['stationCode'])
            if created:
                station.name = station['title'].replace(' %s' % (station['stationCode']), '')
                station.lat = station['lat']
                station.lon = station['lon']
                station.save()
            if val > THRESHOLD_PM10:
                Alert.objects.create(
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


@receiver(post_save, sender=Report)
def on_report_save(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        instance.process_report()

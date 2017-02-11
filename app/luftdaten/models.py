from django.db import models


class SensorValue(models.Model):
    device = models.CharField(max_length=100, db_index=True)
    SDS_P1 = models.FloatField(null=True)
    SDS_P2 = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    samples = models.FloatField()
    min_micro = models.FloatField()
    max_micro = models.FloatField()
    signal = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.created)

class SensorValueAggregated(models.Model):
    device = models.CharField(max_length=100, db_index=True)
    SDS_P1 = models.FloatField(null=True)
    SDS_P2 = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    date = models.DateTimeField()

    def __str__(self):
        return '%s' % (self.date)

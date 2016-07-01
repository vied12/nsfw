from django.db import models


class Station(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return '%s (%s)' % (self.id, self.name)


class PM10(models.Model):
    station = models.ForeignKey(Station)
    value = models.IntegerField()
    date = models.DateField()

    class Meta:
        verbose_name = "PM10"
        verbose_name_plural = "PM10"

    def __str__(self):
        return '%s [%s]: %s' % (self.station.id, self.date, self.value)

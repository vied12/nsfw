from django.core.management.base import BaseCommand
from app.luftdaten.models import SensorValue, SensorValueAggregated
from django.utils import timezone
import datetime


def get_hour(date):
    return timezone.make_aware(
        datetime.datetime(date.year, date.month, date.day, date.hour)
    ) + timezone.timedelta(hours=1)


def merge_rows(rows):
    avgs = {
        'SDS_P1': [],
        'SDS_P2': [],
        'temperature': [],
        'humidity': [],
    }
    for r in rows:
        for k in avgs.keys():
            if getattr(r, k):
                avgs[k].append(getattr(r, k))
    for k in avgs.keys():
        avgs[k] = sum(avgs[k]) / float(len(avgs[k]))
    return avgs


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('device', type=str, help='0')

    def handle(self, *args, **kwargs):
        current_hour = None
        rows_to_merge = []
        rows_to_delete = []
        averages = []
        for row in SensorValue.objects.filter(device=kwargs['device']).order_by('created'):
            date = row.created
            if not current_hour:
                current_hour = get_hour(date)
            if get_hour(date) == current_hour:
                rows_to_merge.append(row)
            else:
                average = merge_rows(rows_to_merge)
                averages.append(average)
                rows_to_delete = rows_to_delete + rows_to_merge
                SensorValueAggregated.objects.get_or_create(device=kwargs['device'], date=current_hour, **average)
                rows_to_merge = [row]
                current_hour = get_hour(date)
        print('averages', len(averages))
        print('rows_to_delete', len(rows_to_delete))
        SensorValue.objects.filter(id__in=[r.id for r in rows_to_delete]).delete()

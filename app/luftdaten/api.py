from .models import SensorValueAggregated
from rest_framework import serializers, viewsets, generics
# from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend


class SensorValueAggregatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorValueAggregated
        fields = '__all__'


# class SensorValueAggregatedViewSet(viewsets.ModelViewSet):
class SensorValueAggregatedViewSet(generics.ListAPIView):
    queryset = SensorValueAggregated.objects.all()
    serializer_class = SensorValueAggregatedSerializer
    filter_fields = ('device',)

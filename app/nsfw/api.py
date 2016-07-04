from .models import Alert, Station, Report
from rest_framework import serializers, viewsets


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'kind', 'date')


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station


class AlertSerializer(serializers.ModelSerializer):
    station = StationSerializer()
    report = ReportSerializer()

    class Meta:
        model = Alert


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_queryset(self):
        id_value = self.request.query_params.get('station', None)
        if id_value:
            id_list = id_value.split(',')
            queryset = Alert.objects.filter(station__in=id_list)
            return queryset

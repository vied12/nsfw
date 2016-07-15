from .models import Alert, Station, Report, Subscription, Email
from rest_framework import serializers, viewsets, mixins
import rest_framework.permissions


class ReportSerializer(serializers.ModelSerializer):
    kind = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ('id', 'kind', 'date')

    def get_kind(self, obj):
        return obj.get_kind_display()


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station


class AlertSerializer(serializers.ModelSerializer):
    report = ReportSerializer()
    station = StationSerializer()

    class Meta:
        model = Alert


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='email.email', read_only=False)

    class Meta:
        fields = ('email', 'station')
        model = Subscription

    def create(self, validated_data):
        email, created = Email.objects.get_or_create(email=validated_data.pop('email')['email'])
        station = validated_data.pop('station')
        sub, created = Subscription.objects.get_or_create(email=email, station=station)
        return sub


class SubscriptionViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (rest_framework.permissions.AllowAny,)


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
            queryset = Alert.objects.filter(station__in=id_list).order_by('-report__date')
            return queryset
        else:
            return Alert.objects.all()

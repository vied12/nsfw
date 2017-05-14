from django.contrib import admin
from .models import SensorValue, SensorValueAggregated


class ReadOnlyAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in obj._meta.fields] + \
            [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False


class SensorValueAdmin(ReadOnlyAdmin):
    list_display = [field.name for field in SensorValue._meta.fields if field.name != 'id']


admin.site.register(SensorValue, SensorValueAdmin)


class SensorValueAggregatedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SensorValueAggregated._meta.fields if field.name != 'id']


admin.site.register(SensorValueAggregated, SensorValueAggregatedAdmin)

from django.contrib import admin
from app.nsfw.models import Station, Report, Alert, Email, Subscription


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'report_count')
    search_fields = ['id', 'name']

    def report_count(self, obj):
        return Alert.objects.filter(station=obj).count()
admin.site.register(Station, StationAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'kind', 'country', 'source')
admin.site.register(Report, ReportAdmin)


class AlertAdmin(admin.ModelAdmin):
    list_display = ('report', 'station', 'value', 'description', 'report_date', 'created', 'updated')
    list_filter = ('report',)

    def report_date(self, obj):
        return obj.report and obj.report.date or ''
admin.site.register(Alert, AlertAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created', 'updated', 'verified')
    list_filter = ('verified',)
admin.site.register(Email, EmailAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('station', 'email', 'messenger')
    list_filter = ('email__email', 'station')
admin.site.register(Subscription, SubscriptionAdmin)

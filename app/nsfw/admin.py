from django.contrib import admin
from app.nsfw.models import Station, Report, Alert, Email, Subscription


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['id', 'name']
admin.site.register(Station, StationAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('kind', 'date')
admin.site.register(Report, ReportAdmin)


class AlertAdmin(admin.ModelAdmin):
    list_display = ('report', 'station', 'value', 'description', 'created', 'updated')
    list_filter = ('report',)
admin.site.register(Alert, AlertAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created', 'updated', 'verified')
    list_filter = ('verified',)
admin.site.register(Email, EmailAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'station')
    list_filter = ('email__email', 'station')
admin.site.register(Subscription, SubscriptionAdmin)

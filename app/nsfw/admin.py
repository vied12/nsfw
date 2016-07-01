from django.contrib import admin
from app.nsfw.models import Station, Report, Alert


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
admin.site.register(Station, StationAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('kind', 'date')
admin.site.register(Report, ReportAdmin)


class AlertAdmin(admin.ModelAdmin):
    list_display = ('report', 'station', 'value', 'description', 'created', 'updated')
admin.site.register(Alert, AlertAdmin)

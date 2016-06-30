from django.contrib import admin
from app.nsfw.models import Station, PM10


class StationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Station, StationAdmin)


class PM10Admin(admin.ModelAdmin):
    pass
admin.site.register(PM10, PM10Admin)

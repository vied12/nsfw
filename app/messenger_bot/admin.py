from django.contrib import admin
from .models import Messenger


class MessengerAdmin(admin.ModelAdmin):
    list_display = ('messenger_id', 'created')

admin.site.register(Messenger, MessengerAdmin)

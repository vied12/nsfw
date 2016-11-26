from django.db import models


class Messenger(models.Model):
    messenger_id = models.CharField(unique=True, max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.messenger_id

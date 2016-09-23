from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    message_text = models.CharField(max_length=200)
    user = models.ForeignKey(User, unique=True)
    channel = models.CharField(max_length=200)
    public_channel = models.BooleanField()
    pub_date = models.DateTimeField(default=django.utils.timezone.now)

import django

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class Message(models.Model):
    message_text = models.CharField(max_length=200)
    user = models.OneToOneField(User, unique=True)
    post_channels = JSONField()
    subscribe_channels = JSONField()
    event = models.CharField(max_length=200)
    public_channel = models.BooleanField()
    pub_date = models.DateTimeField(default=django.utils.timezone.now)

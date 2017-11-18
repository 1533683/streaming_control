from __future__ import unicode_literals
import time
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stream(models.Model):
    name = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    stream_type = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    stream_key = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class History(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.DO_NOTHING, blank=True, null=True)
    date_time = models.IntegerField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    messages = models.TextField(blank=True, null=True)

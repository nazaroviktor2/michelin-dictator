import datetime

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_editor = models.BooleanField(default=False, null=False)
    voicing_time = models.DurationField(default=datetime.timedelta())


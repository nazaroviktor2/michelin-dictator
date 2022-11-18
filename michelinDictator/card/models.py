from django.db import models
from django.conf import settings


# Create your models here.

class Card(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    instruction = models.TextField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "id {0}: {1}".format(self.id, self.name)



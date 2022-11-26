import os
import shutil

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import render

from michelinDictator.settings import MEDIA_ROOT, MEDIA_URL

# Create your models here.
CARD_PATH = "card_{0}"
AUDIO_PATH = CARD_PATH + '/{1}_{2}'


class Card(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    instruction = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "id {0}: {1}".format(self.id, self.name)


def card_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/card_<id>/<filename>
    return AUDIO_PATH.format(instance.card.id, instance.user.id, filename)


@receiver(models.signals.post_delete, sender=Card)
def auto_delete_audio_on_delete(sender, instance, **kwargs):
    """
    Deletes folder from filesystem
    when corresponding `Card` object is deleted.
    """

    path = MEDIA_ROOT + "/" + CARD_PATH.format(instance.id)
    print(path)
    if os.path.isdir(path):
        shutil.rmtree(path)


class Audio(models.Model):
    file_path = models.FileField(upload_to=card_directory_path)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Card:{0} Dictator id:{1}".format(self.card.id, self.user.id)


@receiver(models.signals.post_delete, sender=Audio)
def auto_delete_audio_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Audio` object is deleted.
    """
    print(instance.file_path)
    if instance.file_path:
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)

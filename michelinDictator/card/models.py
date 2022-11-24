from django.db import models
from django.conf import settings
from django.shortcuts import render


# Create your models here.

class Card(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    instruction = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "id {0}: {1}".format(self.id, self.name)


def card_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/card_<id>/<filename>
    return 'card_{0}/{1}_{2}'.format(instance.card.id, instance.user.id, filename)


class Audio(models.Model):

    file_path = models.FileField(upload_to=card_directory_path)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Card:{0} Dictator id:{1}".format(self.card.id, self.user.id)

<<<<<<< HEAD
=======
def home_page(request):
    return render(request, "index.html",{"cards": Card.objects.all()})

def card_page(request):
    id = (request.GET.get("id"))
    all = (Card.objects.get(id=id))
    print("text = ",all.text)
    return render(request,"card.html", {"card":Card.objects.get(id=id)})
>>>>>>> b526357 (back)

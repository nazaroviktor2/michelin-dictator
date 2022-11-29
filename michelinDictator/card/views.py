import datetime
import io
import json
import time
from zipfile import ZipFile
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from django.http import FileResponse
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from card.scripts.add_accent import plus_to_accent
from card.forms import AddCardForm
from card.models import Card, Audio
from card.permissions import IsEditorOrStaffAndAuth, IsOwnerOrStaff
from card.scripts.bold_func import stars_to_highlight
from card.serializers import CardSerializer, AudioSerializer
from michelinDictator.settings import MEDIA_ROOT
from users.forms import RegisterUserForm


# Create your views here.

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsEditorOrStaffAndAuth]
    filterset_fields = ['id', "user", "name"]

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()


class AudioViewSet(ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsOwnerOrStaff]

    filterset_fields = ['id', "user", "card"]

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()




def home_page(request):
    if request.method == "POST":
        print(request.POST)
        action = request.POST.get("action")
        if action == "login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print("valid")
                login(request, user)
                return redirect("home")

        elif action == "registration":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                print("valid")
                form.save()
                return redirect("home")

    return render(request, "index.html", {"cards": Card.objects.all()})


def card_page(request):
    id = (request.GET.get("id"))
    if request.method == "POST":
<<<<<<< HEAD
        print(request.POST)
    return render(request, "card.html", {"card": Card.objects.get(id=id)})
=======
        # print(request.body)
        audios = Audio.objects.filter(card=Card.objects.get(id=id),user=request.user)
        print(audios)
        if audios.first() is not None:
            audios.first().delete()
        audio_file = ContentFile(request.body, name="{0}.wav".format(datetime.date.today()))
        Audio.objects.create(file_path=audio_file, card=Card.objects.get(id=id), user=request.user)


    if request.user.is_authenticated:
        return render(request, "card.html", {"card": Card.objects.get(id=id),
                                             "audios": Audio.objects.filter(card=Card.objects.get(id=id),
                                                                            user=request.user)
                                             })
    else:
        return render(request, "card.html", {"card": Card.objects.get(id=id),
                                             "audios": None
                                             })
>>>>>>> 7546327192b2c681c34678816462560f214f56ef


def add_card(request):
    if request.method == "POST":
        form = AddCardForm(request.POST)

        card = form.save(commit=False)
        card.user = request.user
        text = request.POST.get("text")
        instruction = request.POST.get("instruction")

        if request.POST.get("accent"):
            text = plus_to_accent(text)
            instruction = plus_to_accent(instruction)

        if request.POST.get("highlight"):
            text = stars_to_highlight(text)
            instruction = stars_to_highlight(instruction)

        card.text = text
        card.instruction = instruction

        if form.is_valid():
            card.save()
            return render(request, "successful.html", {"text": "карта для озвучивания создана"})
    return render(request, "add_card.html")


def my_cards(request):
    user = request.user
    return render(request, "my_cards.html", {"cards": Card.objects.filter(user=user)})


def user_card(request):
    id = (request.GET.get("id"))
    if request.method == "POST":
        if request.POST.get("name") == "delete":
            card = Card.objects.get(id=id)
            card.delete()
            return redirect("my_cards")
        elif request.POST.get("name") == "download":
            print(request.user)
            file_name = "all_audio_{0}.zip".format(id)
            zip_file = ZipFile(file_name, 'w')
            audios = Audio.objects.filter(card=Card.objects.get(id=id))
            if audios:
                for audio in audios:
                    path = MEDIA_ROOT + "/" + str(audio.file_path)
                    zip_file.write(path, "{0}.wav".format(audio.id))
                print(zip_file.namelist())
                zip_file.close()
                return FileResponse(open(file_name, "rb"))

    return render(request, "user_card.html", {"card": Card.objects.get(id=id),
                                              "audios": Audio.objects.filter(card=Card.objects.get(id=id))})



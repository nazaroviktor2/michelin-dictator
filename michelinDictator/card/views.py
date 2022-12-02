import datetime

from zipfile import ZipFile
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from card.scripts.add_accent import plus_to_accent
from card.forms import AddCardForm
from card.models import Card, Audio, Video
from card.permissions import IsEditorOrStaffAndAuth, IsOwnerOrStaff
from card.scripts.bold_func import stars_to_highlight
from card.serializers import CardSerializer, AudioSerializer
from michelinDictator.settings import MEDIA_ROOT

# Create your views here.
CARD_ON_PAGE = 5
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


def not_found_page(request,exception):
    return render(request,"not_found.html",status=404)
def home_page(request):
    cards = Card.objects.all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(cards, CARD_ON_PAGE)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "index.html", {"cards": page_obj})


def card_page(request):
    id = (request.GET.get("id"))
    card =get_object_or_404(Card, id=id)
    print(card)
    if  card == Card.objects.none():
        return redirect("not_found")
    if request.user.is_authenticated:
        audio = Audio.objects.filter(card=Card.objects.get(id=id), user=request.user)
        video = Video.objects.filter(card=Card.objects.get(id=id), user=request.user)
        if request.method == "POST":
            now = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            name = request.headers.get("Name")
            if name == "audio":
                duration = request.headers.get("Audio-Time")
                if audio.exists():
                    audio.delete()

                audio_file = ContentFile(request.body, name="{0}.wav".format(now))
                Audio.objects.create(file_path=audio_file, card=Card.objects.get(id=id), user=request.user,
                                                 duration=duration)
            elif name == "Video":
                print("video")
                if video.exists():
                    video.delete()
                video_file = ContentFile(request.body, name="{0}.mp4".format(now))
                Video.objects.create(file_path = video_file,card=Card.objects.get(id=id), user=request.user)



        return render(request, "card.html", {"card": card,
                                             "audios": Audio.objects.filter(card=Card.objects.get(id=id),
                                                                            user=request.user),
                                             "videos": Video.objects.filter(card=Card.objects.get(id=id),
                                                                            user=request.user)
                                             })
    else:
        return render(request, "card.html", {"card": card,
                                             "audios": None,
                                             "videos": None,
                                             })


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
    cards = Card.objects.filter(user=user)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(cards, CARD_ON_PAGE)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "my_cards.html", {"cards": page_obj})


def my_audios(request):
    user = request.user
    card_id = [audio.card.id for audio in Audio.objects.filter(user=user)]

    res = []
    for id in card_id:
        res.append(Card.objects.get(id=id))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(res, CARD_ON_PAGE)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    # return render(request, "index.html", {"cards": page_obj})

    return render(request, "my_audios.html", {"cards": page_obj})


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

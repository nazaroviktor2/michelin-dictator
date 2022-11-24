<<<<<<< HEAD
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
=======
from django.shortcuts import render
>>>>>>> b526357 (back)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from card.models import Card, Audio
from card.permissions import IsEditorOrStaffAndAuth, IsOwnerOrStaff
from card.serializers import CardSerializer, AudioSerializer
<<<<<<< HEAD
from users.forms import RegisterUserForm
=======
>>>>>>> b526357 (back)


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
<<<<<<< HEAD

def home_page(request):
    if request.method == "POST":
        print("post zapros")
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
    all = (Card.objects.get(id=id))
    print("text = ",all.text)
    return render(request,"card.html", {"card":Card.objects.get(id=id)})
=======
>>>>>>> b526357 (back)

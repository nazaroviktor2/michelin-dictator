from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from card.models import Card, Audio
from card.permissions import IsEditorOrStaffAndAuth, IsOwnerOrStaff
from card.serializers import CardSerializer, AudioSerializer


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

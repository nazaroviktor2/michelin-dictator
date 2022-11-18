from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from card.models import Card
from card.serializers import CardSerializer


# Create your views here.

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

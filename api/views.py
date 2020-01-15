from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PlayerSerializer
from data.models import Upgrade, Ship, Skill, Clan, Player, ShipInstance
from clan_battles.models import Battle, ClanInstance, PlayerInstance

# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
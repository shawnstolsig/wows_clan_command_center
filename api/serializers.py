from data.models import Upgrade, Ship, Skill, Clan, Player, ShipInstance
from clan_battles.models import Battle, ClanInstance, PlayerInstance
from rest_framework import serializers

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        # ommitted fields: player_user, player_ships, player_clan
        fields = ('player_wgid', 'player_nickname', 'player_clan_role', 'player_joined_at')
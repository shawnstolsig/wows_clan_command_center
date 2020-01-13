from django.db import models
from data.models import Clan
from profiles.models import Profile


# Battle: a particular clan battle that was played
class Battle(models.Model):

    # identifiers
    battle_wgid = models.IntegerField()

    # characteristics
    battle_map = models.CharField(max_length=50)
    battle_realm = models.CharField(max_length=10)
    battle_arena_id = models.IntegerField()
    battle_finished_at = models.DateTimeField()
    battle_season_number = models.IntegerField()

    # date created (for potential future DB maintenance)
    date_created = models.DateTimeField(auto_now_add=True)

# A clan's participation in a clan battle
class ClanInstance(models.Model):

    # identifier
    claninstance_wgid = models.IntegerField()

    # characteristics 
    claninstance_clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True)      # if clan is deleted, keep the ClanInstance for data purposes
    claninstance_battle = models.ForeignKey(Battle, on_delete=models.SET_NULL, null=True)   # if battle is deleted, keep the ClanInstance for data purposes
    claninstance_team_no = models.IntegerField()        # two teams per clan battle, so this will be with 1 or 2.  team 1 will be player's clan
    claninstance_division = models.IntegerField()       
    claninstance_league = models.IntegerField()
    claninstance_rating_delta = models.IntegerField()
    claninstance_result = models.CharField(max_length=10)

    # date created (for potential future DB maintenance)
    date_created = models.DateTimeField(auto_now_add=True)

# A player's participation in a clan battle
class PlayerInstance(models.Model):

    # identifiers

    # characteristics
    playerinstance_clan = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)             # if player's profile deleted, keep this PlayerInstance for data purposes              
    playerinstance_claninstance = models.ForeignKey(ClanInstance, on_delete=models.SET_NULL, null=True) # if battle is deleted, delete the PlayerInstance

    # date created (for potential future DB maintenance)
    date_created = models.DateTimeField(auto_now_add=True)

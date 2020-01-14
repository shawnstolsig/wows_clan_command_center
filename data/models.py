from django.db import models
from clan.models import UserClan

# Upgrade: for each upgrade slot in the game
class Upgrade(models.Model):

    # upgrade identifiers
    upgrade_id = models.IntegerField()
    upgrade_name = models.CharField(max_length=50)
    
    # store when upgrade added to database (in case it needs to be deleted later)
    date_created = models.DateTimeField(auto_now_add=True)

# Ship: data for each ship in the game
class Ship(models.Model):

    # ship identifiers
    ship_id = models.IntegerField()
    ship_name = models.CharField(max_length=50)

    # ship characteristics
    ship_class = models.CharField(max_length=2)     # options: CV, BB, CA, DD, SS
    ship_tier = models.IntegerField()
    ship_nation = models.CharField(max_length=50)
    # ship_upgrades = models.ManyToManyField(Upgrade, related_name="ship_upgrades")
    ship_upgrade_slots = models.IntegerField()

    # store when ship added to database (in case it needs to be deleted later)
    date_created = models.DateTimeField(auto_now_add=True)


# Skill: commander skills
class Skill(models.Model):

    # skill characteristics
    skill_id = models.IntegerField()
    skill_name = models.CharField(max_length=100)
    skill_tier = models.IntegerField()
    skill_picture_url = models.URLField()

    # store when skill added to database (in case it needs to be deleted later)
    date_created = models.DateTimeField(auto_now_add=True)

# Clan: one created for each clan in the game.
class Clan(models.Model):

    # identifier
    clan_wgid = models.IntegerField()               
    clan_tag = models.CharField(max_length = 10)    # e.g. "KSD"
    clan_name = models.CharField(max_length = 50)   # e.g. "Kill Steal Denied"

    # characteristics
    clan_members_count = models.IntegerField()
    clan_realm = models.CharField(max_length = 10)

    # store when skill added to database (in case it needs to be deleted later)
    date_created = models.DateTimeField(auto_now_add=True)

# Player: a Player will be created for each player in each website user's clan
# This will be helpful for storing CB specific info (ship list, stats, etc) even if they 
# are not users of the site themselves
class Player(models.Model):

    # identifier
    player_wgid = models.IntegerField()
    # player_nickname = models.CharField(max_length=50)

    # characteristics
    # player_profile = models.OneToOneField(Profile, on_cascade=models.SET_NULL, null=True)   # links to website profile, if it exists
    player_clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True)
    player_userclan = models.ForeignKey(UserClan, on_delete=models.SET_NULL, null=True)
    player_ships = models.ManyToManyField(Ship, null=True)
    player_clan_role = models.CharField(max_length=20, null=True)
    player_joined_at = models.IntegerField(null=True)

    # store when skill added to database (in case it needs to be deleted later)
    date_created = models.DateTimeField(auto_now_add=True)

# ShipInstance: a ship owned by a specific player (extends Ship to include stats)
class ShipInstance(models.Model):

    # identifiers
    shipinstance_ship = models.ForeignKey(Ship, on_delete=models.SET_NULL, null=True)
    shipinstance_player = models.ForeignKey(Player, on_delete=models.CASCADE)

    # characteristics
    shipinstance_main_battery_hits = models.IntegerField(null=True)
    shipinstance_main_battery_shots = models.IntegerField(null=True)
    shipinstance_xp = models.IntegerField(null=True)
    shipinstance_battles = models.IntegerField(null=True)
    shipinstance_torpedoes_hits = models.IntegerField(null=True)
    shipinstance_torpedoes_shots = models.IntegerField(null=True)
    shipinstance_wins = models.IntegerField(null=True)
    shipinstance_losses = models.IntegerField(null=True)
    shipinstance_damage_dealt = models.IntegerField(null=True)
    shipinstance_potential_damage = models.IntegerField(null=True)
    shipinstance_spotting_damage = models.IntegerField(null=True)
    shipinstance_cb_battles = models.IntegerField(default=0)
    shipinstance_cb_wins = models.IntegerField(default=0)
    shipinstance_cb_battles_survived = models.IntegerField(default=0)

    # for db maintainence
    date_created = models.DateTimeField(auto_now_add=True) 

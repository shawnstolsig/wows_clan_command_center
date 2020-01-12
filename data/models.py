from django.db import models

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



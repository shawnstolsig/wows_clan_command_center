from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .config import api_key
from .models import Upgrade, Ship, Skill
import requests
import json

# Create your views here.
def update_game_data(request, region):
    print("Updating game data...")

    # resolve region
    if region == 'NA':
        realm = 'com'
    elif region == 'EU':
        realm = 'eu'
    elif region == 'SEA':
        realm = 'asia'

    # ------------------ get all ship data:-----------------------
    ship_data = {}
    # API will return status of "error" when you request an empty page and "ok" otherwise.  Use status as flag for while loop
    status = "ok"
    page_num = 1
    # loop until invalid page is requested
    while status == "ok":
        payload = {
            'application_id': api_key,
            'fields': 'name,type,tier,nation,upgrades,mod_slots',
            'page_no': page_num
        }
        response = requests.get(f"https://api.worldofwarships.{realm}/wows/encyclopedia/ships/", params=payload)
        page_query = json.loads(response.text)

        # add each ship to master ship data dictionary
        if page_query['status'] == "ok":
            for ship in page_query['data']:
                ship_data[ship] = page_query['data'][ship] 

        # update loop variables
        page_num += 1
        status = page_query['status']

    # add ships to DB
    added_to_db_counter = 0
    for ship in ship_data:
        s, was_created = Ship.objects.get_or_create(
            ship_id=ship,
            ship_name=ship_data[ship]['name'],
            ship_class=ship_data[ship]['type'],
            ship_tier=ship_data[ship]['tier'],
            ship_nation=ship_data[ship]['nation'],
            # ship_upgrades=ship_data[ship]['upgrades'],                 WILL NEED TO FIGURE HOW TO LOOP THROUGH THESE
            ship_upgrade_slots=ship_data[ship]['mod_slots'],
        )
        if was_created:
            added_to_db_counter += 1

    # verify ship load was successful
    print(f'{len(ship_data)} ships loaded from WG API, {page_num-1} pages.  {added_to_db_counter} new DB additions')

    # ------------------ get all skill data:-----------------------
    payload = {
        'application_id': api_key,
        'fields': 'name,tier,icon',
    }
    response = requests.get(f"https://api.worldofwarships.{realm}/wows/encyclopedia/crewskills/", params=payload)
    page_query = json.loads(response.text)

    # add skills to DB
    added_to_db_counter = 0
    for skill in page_query['data']:
        s, was_created = Skill.objects.get_or_create(
            skill_id=skill,
            skill_name=page_query['data'][skill]['name'],
            skill_tier=page_query['data'][skill]['tier'],
            skill_picture_url=page_query['data'][skill]['icon'],
        )
        if was_created:
            added_to_db_counter += 1

    # verify skill load was successful
    print(f'{len(page_query["data"])} skills loaded from WG API, {added_to_db_counter} new DB additions')

    return HttpResponseRedirect(reverse('clan_battles:dashboard'))
    
class SettingsView(TemplateView):
    template_name = 'settings.html'
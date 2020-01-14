from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .config import api_key
from .models import Upgrade, Ship, Skill, Clan, Player
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

    update_ships(realm)
    update_skills(realm)
    update_clans()

    return HttpResponseRedirect(reverse('clan_battles:dashboard'))
    
class SettingsView(TemplateView):
    template_name = 'settings.html'


# functions for updating different parts of the game
def update_ships(realm):
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


def update_skills(realm):
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

def update_clans():
    # unlike other data update functions, must update clans across all four realms (due to cross-server CB)


    # ------------------ get all clan data:-----------------------
    added_to_db_counter = 0         # number added to db
    counter = 0                     # total number for WG API
    for realm in ['com', 'ru', 'eu', 'asia']:
        # add clans to DB.  API returns list of up to 100 ("count") of clans at a time
        page_num = 1                    # page num sent to API.  currently about 145 pages of clans in NA
        count = 100                     # count of clans per page.  usually 100, but drops to 0 once all clans have been listed
        while count != 0:
            payload = {
                'application_id': api_key,
                'page_no': page_num,
            }
            response = requests.get(f"https://api.worldofwarships.{realm}/wows/clans/list/", params=payload)
            page_query = json.loads(response.text)

            for clan in page_query['data']:
                counter += 1
                if realm == 'com':
                    pretty_realm = 'NA'
                elif realm == 'ru':
                    pretty_realm = 'RU'
                elif realm == 'eu':
                    pretty_realm = 'EU'
                elif realm == 'asia':
                    pretty_realm = 'SEA'

                c, was_created = Clan.objects.get_or_create(
                    clan_wgid = clan['clan_id'],
                    clan_tag = clan['tag'],
                    clan_name = clan['name'],
                    clan_members_count = clan['members_count'],
                    clan_realm = pretty_realm,
                )
                if was_created:
                    added_to_db_counter += 1

            # print status message to console every 500 clans
            if counter % 500 == 0:
                print(f"Retrieved {counter} of {page_query['meta']['total']} clans from {pretty_realm} server.")

            # update loop vars        
            page_num += 1
            count = page_query['meta']['count']

        # completed realm message
        print(f"Completed retrieving {page_query['meta']['total']} clans from {pretty_realm} server.")

    # verify clan load was successful
    print(f'{counter} clans across all realms, from WG API. {added_to_db_counter} new DB additions')


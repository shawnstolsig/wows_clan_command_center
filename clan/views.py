from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from .models import UserClan
from data.models import Ship, ShipInstance, Player, Clan
from data.config import api_key
import requests
import json

# For displaying the clan dashboard template
class Dashboard(TemplateView):
    template_name = "clan.html"

# For updating the signed in user's Clan (and clan's Player, including their ships) info
def update_clan(request, region):
    # status message
    print(f"Updating {request.user.username}'s clan information...'")

    # resolve region
    if region == 'NA':
        realm = 'com'
    elif region == 'EU':
        realm = 'eu'
    elif region == 'SEA':
        realm = 'asia'

    # ------------------ create players for logged in user's clan:-----------------------
    # get all players in user's clan
    players_clan = request.user.profile.clan_id
    payload = {
        'application_id': api_key,
        'clan_id': players_clan,
        'fields': 'members_ids',
    }
    response = requests.get(f"https://api.worldofwarships.{realm}/wows/clans/info/", params=payload)
    page_query = json.loads(response.text)
    player_list = page_query['data'][str(players_clan)]['members_ids']
    
    #status message
    print(f"Total players in {Clan.objects.get(clan_wgid=request.user.profile.clan_id)}: {len(player_list)}")
    
    # turn player_list into a payload
    player_list_payload = ''
    for player in player_list:
        player_list_payload += f'{player},'

    # get clan details for all players, mainly their roles.  all of the clan's players will be sent at once in the payload
    payload = {
        'application_id': api_key,
        'account_id': player_list_payload,
    }
    response = requests.get(f"https://api.worldofwarships.{realm}/wows/clans/accountinfo/", params=payload)
    page_query = json.loads(response.text)

    # for each player, create a Player object (if it doesn't already exist).  Update all Players, either way. 
    count_added_to_db = 0
    for player in page_query['data']:
        p, was_created = Player.objects.get_or_create(player_wgid = int(player))
        update_player_info(realm, p, players_clan, page_query['data'][player]['role'], page_query['data'][player]['joined_at'])
        
        if was_created:
            count_added_to_db += 1

    # status message
    print(f"Players added to db: {count_added_to_db}")
    print("Completed updating user's clan information")

    return HttpResponseRedirect(reverse('clan:dashboard'))

def update_player_info(realm, p, players_clan, clan_role, joined_date):
    # player object p is passed in
    testclan = Clan.objects.get(clan_wgid=players_clan)
    p.player_clan = Clan.objects.get(clan_wgid=players_clan)
    # p.player_userclan = UserClan.objects.get(userclan_wgid=players_clan)
    p.player_clan_role = clan_role
    p.player_joined_at = joined_date

    # update ships
    payload = {
        'application_id': api_key,
        'account_id': p.player_wgid,
    }
    response = requests.get(f"https://api.worldofwarships.{realm}/wows/ships/stats/", params=payload)
    page_query = json.loads(response.text)

    added_to_db_counter = 0
    ship_list = page_query['data'][str(p.player_wgid)]
    for ship in ship_list:
        try:
            s, was_created = ShipInstance.objects.get_or_create(
                shipinstance_player = p,
                shipinstance_ship = Ship.objects.get(ship_id=ship['ship_id'])
                )
            update_ship_stats(realm, s, ship)
            if was_created:
                added_to_db_counter += 1
        except Ship.DoesNotExist:
            print(f"{ship['ship_id']} does not match to ship in encyclopedia")


    print(f"Finished loading player ships. Player {p.player_wgid} has {len(page_query['data'][str(p.player_wgid)])} ships. {added_to_db_counter} are new and were added to db.")

    p.save()

def update_ship_stats(realm, s, ship):
    # update ship stats
    payload = {
        'application_id': api_key,
        'account_id': s.shipinstance_player.player_wgid,
    }
    response = requests.get(f"https://api.worldofwarships.{realm}/wows/ships/stats/", params=payload)
    page_query = json.loads(response.text)

    s.shipinstance_main_battery_hits = ship['pvp']['main_battery']['hits']
    s.shipinstance_main_battery_shots = ship['pvp']['main_battery']['shots']
    s.shipinstance_xp = ship['pvp']['xp']
    s.shipinstance_battles = ship['pvp']['battles']
    s.shipinstance_torpedoes_hits = ship['pvp']['torpedoes']['hits']
    s.shipinstance_torpedoes_shots = ship['pvp']['torpedoes']['shots']
    s.shipinstance_wins = ship['pvp']['wins']
    s.shipinstance_losses = ship['pvp']['losses']
    s.shipinstance_damage_dealt = ship['pvp']['damage_dealt']
    s.shipinstance_potential_damage = ship['pvp']['max_total_agro']
    s.shipinstance_spotting_damage = ship['pvp']['damage_scouting']
    s.save()
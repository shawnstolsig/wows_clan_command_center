from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from .models import Battle
import requests
import json

# main CB dashboard
class DashboardView(TemplateView):
    template_name = "dashboard.html"

# get last 50 alpha and bravo battles
def get_battles(request, region):

    # resolve region
    if region == 'NA':
        realm = 'com'
    elif region == 'EU':
        realm = 'eu'
    elif region == 'SEA':
        realm = 'asia'

    payload = {
        'team': 1,
    }
    # commenting this out until season begins, unable to test between seasons
    # response = requests.get(f"https://clans.worldofwarships.{realm}/clans/wows/ladder/api/battles/", params=payload)
    # page_query = json.loads(response.text)

    with open('sample_data.json') as json_file:
        page_query = json.load(json_file)    
    
    print("loaded battle page")
    print(page_query)

    # add battles to DB
    # added_to_db_counter = 0
    # for battle in page_query['data']:
    #     s, was_created = Skill.objects.get_or_create(
    #         skill_id=skill,
    #         skill_name=page_query['data'][skill]['name'],
    #         skill_tier=page_query['data'][skill]['tier'],
    #         skill_picture_url=page_query['data'][skill]['icon'],
    #     )
    #     if was_created:
    #         added_to_db_counter += 1

    # verify skill load was successful
    # print(f'{len(page_query["data"])} skills loaded from WG API, {added_to_db_counter} new DB additions')

    return HttpResponseRedirect(reverse('clan_battles:dashboard'))
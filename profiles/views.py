from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from openid_wargaming.authentication import Authentication

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

def test_openid(request):
    return_to = 'http://localhost:8000/'
    auth = Authentication(return_to=return_to)
    
    url = auth.authenticate('https://na.wargaming.net/id/openid')

    return HttpResponseRedirect(url)
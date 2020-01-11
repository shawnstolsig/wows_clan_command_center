from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from .authentication import Authentication
from .verification import Verification
from django.urls import reverse
import re

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

def openid_send(request):
    return_to = 'http://localhost:8000/profiles/openid/return/'
    auth = Authentication(return_to=return_to)
    url = auth.authenticate('https://na.wargaming.net/id/openid/')
    # url = auth.authenticate('https://api.worldoftanks.com/wot/auth/login/?application_id=cdcbc9fdb2ee0eb2f701d4622deb485c')
    return HttpResponseRedirect(url)

def openid_return(request):
    # get current url
    # current_url = request.get_full_path()
    current_url = request.build_absolute_uri()
    print(f"response full path is {current_url}")
    verify = Verification(current_url)
    identities = verify.verify()
    print(f"identies are {identities}")
    # pull out some information from the response
    # regex expression to parse return
    regex = r'https://na.wargaming.net/id/([0-9]+)-(\w+)/'
    match = re.search(regex, identities['identity'])
    print(f"match is {match}")
    account_id = match.group(1)
    nickname = match.group(2)

    # handle site-side login here?  match with profile?

    # NEXT STEP....HOW TO GET IT TO SAVE COOKIES OR SESSION INFO SO THAT YOU ARE LOGGED IN WHEN REDIRECTED TO WG
    # set session information to db
    print(f"request.session is {request.session.__dict__}")
    request.session['account_id'] = account_id
    request.session['nickname'] = nickname

    return HttpResponseRedirect(reverse('profiles:login_success', args=(nickname,)))

def login_success(request, nickname):
    try:
        context = { 'nickname': nickname }
        return render(request, "landing.html", context)
    except KeyError:
        return HttpResponse(status=400)

    # return HttpResponseRedirect("https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=1")
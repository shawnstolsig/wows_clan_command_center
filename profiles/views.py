from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


class DetailPlayerView(TemplateView):
    template_name = "profile.html"

def printrequest(request):
    print("back from api login")
    print(request.GET['access_token'])
    return render(request, "return.html", {'access_key': request.GET['access_token']})
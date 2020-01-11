from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

# Create your views here.
class DashboardView(TemplateView):
    template_name = "dashboard.html"
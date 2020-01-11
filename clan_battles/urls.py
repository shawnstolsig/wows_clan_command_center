from django.urls import path
from . import views

app_name = 'clan_battles'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]

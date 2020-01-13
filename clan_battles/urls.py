from django.urls import path
from . import views

app_name = 'clan_battles'
urlpatterns = [
    path('getbattles/', views.get_battles, name='get_battles'),
    path('', views.DashboardView.as_view(), name='dashboard'),
]

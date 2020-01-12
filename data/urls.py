from django.urls import path
from . import views

app_name = 'data'
urlpatterns = [
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('<str:region>/', views.update_game_data, name='update_game_data'),
]

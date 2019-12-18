from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('openid/', views.test_openid, name='wows_login'),
]

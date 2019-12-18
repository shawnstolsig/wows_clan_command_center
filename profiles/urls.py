from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('openid/', views.openid_send, name='wows_login'),
    path('openid/return/', views.openid_return, name='wows_login_return'),
    path('openid/login_success/<str:nickname>/', views.login_success, name='login_success'),
]

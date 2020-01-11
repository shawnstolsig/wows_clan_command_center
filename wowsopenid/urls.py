from django.urls import path
from . import views

app_name = 'wowsopenid'
urlpatterns = [
    path('', views.FirstStep.as_view(), name='first'),
    path('callback', views.SecondStep.as_view(), name='callback'),
    path('logout', views.logout_user, name='logout')
]

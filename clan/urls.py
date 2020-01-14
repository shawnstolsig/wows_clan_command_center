from django.urls import path
from . import views

app_name = "clan"
urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('updateclan/<str:region>', views.update_clan, name="update"),
]
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.stations_overview, name='stations_overview'),
]

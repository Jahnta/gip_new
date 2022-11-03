from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.units_overview, name='units_overview'),
    path('add/<int:station_id>', views.unit_add, name='unit_add'),
]

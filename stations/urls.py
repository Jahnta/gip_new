from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.stations_overview, name='stations_overview'),
    path('add/', views.station_add, name='station_add'),
    path('<int:station_id>/', views.station_detail, name='station_detail'),
    path('<int:station_id>/edit/', views.station_edit, name='station_edit'),
    path('<int:station_id>/delete/', views.station_delete, name='station_delete'),
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('chart/', views.event_chart, name='event_chart'),
    path('add/', views.event_add, name='event_add'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
]

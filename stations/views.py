from django.shortcuts import render
from .models import Station

def stations_overview(request):
    station_list = Station.objects.all()
    data = {'stations' : station_list}
    return render(request, 'stations/overview.html', data)

# Create your views here.

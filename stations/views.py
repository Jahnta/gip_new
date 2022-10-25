from django.shortcuts import render
from .models import Station

def stations_overview(request):
    company_list = [x[0] for x in set(list(Station.objects.order_by('id').values_list('company')))]
    companies = []
    for company in sorted(company_list):
        stations = []
        station_list = Station.objects.filter(company=company)
        company_data = {
            'name' : company,
            'station_list' : station_list
        }
        companies.append(company_data)
    data = {
        'companies' : companies,
    }
    return render(request, 'stations/overview.html', data)

# Create your views here.

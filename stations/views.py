from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import StationForm
from .models import Company, Station


def stations_overview(request):
    stations = []
    data = {'companies': []}
    queryset = Station.objects.select_related('company').all()
    for station in queryset:
        stations.append(
            {
                'id' : station.id,
                'name' : station.name,
                'address' : station.address,
                'company' : (station.company.name if station.company else 'Прочие'),
                'image_url' : (station.image.url if station.image else ''),
            }
        )
    companies = set(x['company'] for x in stations)
    for company in sorted(companies):
        company_data = {
            'name' : company,
            'station_list': [x for x in stations if x['company'] == company]
        }
        data['companies'].append(company_data)
    return render(request, 'stations/station-overview.html', data)


def station_detail(request, station_id):
    station = get_object_or_404(Station, pk=station_id)
    data = {
        'station': station,
    }
    return render(request, 'stations/station-detail.html', data)


@staff_member_required
def station_edit(request, station_id):
    error = ''
    station = get_object_or_404(Station, pk=station_id)
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES, instance=station)
        if form.is_valid():
            try:
                image = request.FILES['image']
            except:
                pass
            station = form.save()
            return redirect('station_detail', station_id=station_id)
        else:
            error = 'Форма заполнена неправильно'
    else:
        form = StationForm(instance=station)
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'stations/station-edit.html', data)


@staff_member_required
def station_add(request):
    error = ''
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                station = Station(image=request.FILES['image'])
            except:
                pass
            station = form.save()
            return redirect('station_detail', station_id=station.id)
        else:
            error = 'Форма заполнена неправильно'
    else:
        form = StationForm()
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'stations/station-add.html', data)


@staff_member_required
def station_delete(request, station_id):
    station = get_object_or_404(Station, pk=station_id)
    form = StationForm()
    if request.method == 'POST':
        station.delete()
        return redirect('stations_overview')
    data = {
        'form': form,
    }
    return render(request, 'stations/station-delete.html', data)

# Create your views here.

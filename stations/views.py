from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from events.models import Event
from .forms import StationForm, UnitForm
from .models import Company, Station, Unit, UnitType


def stations_overview(request):
    stations = []
    data = {'companies': []}
    queryset = Station.objects.select_related('company')
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
    station = get_object_or_404(
        Station.objects.select_related('company').prefetch_related(
            Prefetch('unit_set', queryset=Unit.objects.order_by('id').select_related('unit_type').prefetch_related(
                Prefetch('event_set', queryset=Event.objects.order_by('start__year').select_related('event_type'), to_attr='prefetched_events'),
            ), to_attr='prefetched_units'
        )
    ), pk=station_id)

    events = []
    for unit in station.prefetched_units:
        for event in unit.prefetched_events:
            events.append(event)
    data = {
        'station': station,
        'units': station.prefetched_units,
        'events': events,
    }
    return render(request, 'stations/station-detail.html', data)


@staff_member_required
def station_edit(request, station_id):
    error = ''
    station = get_object_or_404(Station, pk=station_id)
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES, instance=station)
        if form.is_valid():
            station = form.save()
            return redirect('station_detail', station_id=station.id)
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
    if request.method == 'POST':
        station.delete()
        return redirect('stations_overview')
    data = {
        'station': station,
    }
    return render(request, 'stations/station-delete.html', data)


def units_overview(request):

    units = []
    unit_types = []
    stations = []

    queryset = Unit.objects.select_related('station', 'unit_type')
    for unit in queryset:
        units.append(
            {
                'id': unit.id,
                'name': unit.name,
                'unit_type': unit.unit_type,
                'station': unit.station,
            }
        )
        if unit.unit_type not in unit_types:
            unit_types.append(unit.unit_type)
        if unit.station not in stations:
            stations.append(unit.station)

    data1 =[]
    for unit_type in unit_types:
        unit_type_station_list = []
        unit_type_counter = 0
        for station in stations:
            station_unit_list = []
            for unit in units:
                if unit['unit_type'] == unit_type and unit['station'] == station:
                    station_unit_list.append(unit)
                    unit_type_counter += 1
            if station_unit_list:
                unit_type_station_list.append({'station': station, 'units': station_unit_list})
        data1.append(
            {'unit_type': unit_type,
             'stations': sorted(unit_type_station_list, key=lambda x: x['station'].id),
             'counter' : unit_type_counter}
        )
    data = {
        'unit_types': data1,
    }
    return render(request, 'stations/unit-overview.html', data)


def unit_detail(request, station_id, unit_id):
    unit = get_object_or_404(Unit.objects.prefetch_related('event_set'), pk=unit_id)

    data = {
        'unit': unit,
        'events': unit.event_set.all()
    }
    return render(request, 'stations/unit-detail.html', data)


@staff_member_required
def unit_edit(request, station_id, unit_id):
    error = ''
    unit = get_object_or_404(Unit.objects.select_related('station'), pk=unit_id)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.name = str(unit.unit_type) + ' ст. № ' + str(unit.station_number)
            unit.short_name = 'ГТ-' + str(unit.station_number)
            unit = form.save()
            return redirect('unit_detail', unit_id=unit.id, station_id=station_id)
        else:
            error = 'Форма заполнена неправильно'
    else:
        form = UnitForm(instance=unit)
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'stations/unit-edit.html', data)


@staff_member_required
def unit_add(request, station_id):
    error = ''
    initial_data = {
            'station': station_id,
        }
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.name = str(unit.unit_type) + ' ст. № ' + str(unit.station_number)
            unit.short_name = 'ГТ-' + str(unit.station_number)
            unit = form.save()
            return redirect('unit_detail', unit_id=unit.id, station_id=unit.station.id)
        else:
            error = 'Форма заполнена неправильно'
    else:
        form = UnitForm(initial=initial_data)
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'stations/unit-add.html', data)


@staff_member_required
def unit_delete(request, station_id, unit_id):
    unit = get_object_or_404(Unit.objects.select_related('station'), pk=unit_id)
    form = UnitForm()
    if request.method == 'POST':
        unit.delete()
        return redirect('units_overview')
    data = {
        'form': form,
        'unit': unit,
    }
    return render(request, 'stations/unit-delete.html', data)

# Create your views here.

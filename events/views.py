from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from stations.models import Unit, Station
from .forms import EventForm
from .models import Event


def event_chart(request):
    station_list = Station.objects.order_by('id').prefetch_related(
        Prefetch('unit_set', queryset=Unit.objects.order_by('id').select_related('unit_type').prefetch_related(
            Prefetch('event_set', queryset=Event.objects.order_by('start').select_related('event_type'), to_attr="prefetched_events")
        ), to_attr="prefetched_units")
    )

    year_list = []

    for station in station_list:
        for unit in station.prefetched_units:
            for event in unit.prefetched_events:
                if event.start.year not in year_list:
                    year_list.append(event.start.year)
                if event.end.year not in year_list:
                    year_list.append(event.end.year)

    years = []
    for year in sorted(year_list):
        stations = []
        for station in station_list:
            units = []
            unit_list = station.prefetched_units
            for unit in unit_list:
                events = []
                for event in unit.prefetched_events:
                    if event.start.year == year or event.end.year == year:
                        events.append(event)
                unit_dict = {'unit': unit, 'events': events}
                units.append(unit_dict)
            station_dict = {'station': station, 'units': units}
            stations.append(station_dict)
        year_dict = {'year': year, 'stations': stations}
        years.append(year_dict)
    data = {'years': years}

    return render(request, 'events/event-chart.html', data)


def event_detail(request, event_id):
    event = get_object_or_404(Event.objects.select_related('unit__station', 'event_type'), pk=event_id)
    data = {
        'event': event
    }
    return render(request, 'events/event-detail.html', data)


@staff_member_required
def event_edit(request, event_id):
    error = ''
    event = get_object_or_404(Event.objects.select_related('unit__station', 'event_type'), pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.duration = (event.end - event.start).days + 1
            event = form.save()
            return redirect('event_detail', event_id=event.id)
        else:
            error = 'Форма заполнена неправильно'
    else:
        form = EventForm(instance=event)
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'events/event-edit.html', data)


@staff_member_required
def event_add(request):
    error = ''
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.duration = (event.end - event.start).days + 1
            event = form.save()
            return redirect('event_detail', event_id=event.id)
        else:
            error = 'Форма заполнена неправильно'
    else:
        form = EventForm()
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'events/event-add.html', data)


@staff_member_required
def event_delete(request, event_id):
    event = get_object_or_404(Event.objects.select_related('unit__station', 'event_type'), pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_chart')
    data = {
        'event': event,
    }
    return render(request, 'events/event-delete.html', data)

# Create your views here.

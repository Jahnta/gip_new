from django import forms

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'unit',
            'event_type',
            'start',
            'end',
        ]
        help_texts = {
            'unit' : 'Имя установки',
            'event_type': 'Тип события',
            'start': 'Дата начала события',
            'end': 'Дата окончания события',
        }
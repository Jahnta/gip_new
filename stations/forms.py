from django import forms

from .models import Station, Unit


class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = [
            'company',
            'id',
            'name',
            'short_name',
            'address',
            'image',
        ]
        help_texts = {
            'id' : 'Идентификатор в формате ХХХ, первая цифра - код компании, вторая и третья - код станции',
            'name': 'Полное наименование станции, например "ТЭЦ-9 - филиал ПАО "Мосэнерго"',
            'short_name': 'Короткое наименование станции, например "ТЭЦ-9"',
            'company': 'Наименование компании, например "ПАО "Мосэнерго""',
            'address': 'Адрес нахождения',
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'station',
            'unit_type',
            'station_number'
        ]

        help_texts = {
            'station': 'Наименование станции, например "ТЭЦ-9"',
            'unit_type': 'Тип установки',
            'station_number': 'Станционный номер'
        }
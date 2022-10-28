from django import forms

from .models import Station

class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = [
            'id',
            'name',
            'short_name',
            'company',
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
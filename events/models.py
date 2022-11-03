from django.db import models

from stations.models import Unit


class EventType(models.Model):
    name = models.CharField('Имя события', max_length=100)
    short_name = models.CharField('Короткое имя события', max_length=100)

    def __str__(self):
        return self.short_name

    class Meta:

        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы события'

class Event(models.Model):
    event_type = models.ForeignKey(
        EventType,
        verbose_name='Тип события',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name='Установка',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start = models.DateField(verbose_name='Дата начала')
    end = models.DateField(verbose_name='Дата окончания')
    duration = models.IntegerField(verbose_name='Длительность')

    def __str__(self):
        return f'{self.event_type.short_name} {self.unit.short_name} {self.unit.station.short_name} {self.start.year}'

    class Meta:

        verbose_name = 'Событие'
        verbose_name_plural = 'События'


# Create your models here.

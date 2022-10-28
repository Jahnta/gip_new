from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField('Наименование компании', max_length=100)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Station(models.Model):
    id = models.IntegerField('Ид.', primary_key=True)
    name = models.CharField('Наименование станции', max_length=100)
    short_name = models.CharField('Короткое наименование станции', max_length=10, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField('Адрес нахождения', max_length=100, null=True, blank=True)
    image = models.ImageField('Изображение', blank=True, upload_to='img/')

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'


class UnitType(models.Model):
    machine_type = models.CharField('Тип машины', max_length=50, default='Газотурбинная установка')
    name = models.CharField('Имя установки', max_length=10, default='-')

    def __str__(self):
        return self.machine_type + ' ' + self.name

    class Meta:

        verbose_name = 'Тип установки'
        verbose_name_plural = 'Типы установок'


class Unit(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    name = models.CharField('Наименование установки', max_length=100)
    short_name = models.CharField('Короткое наименование установки', max_length=10)
    unit_type = models.ForeignKey(UnitType, on_delete=models.SET_NULL, null=True, blank=True)
    station_number = models.CharField('Станционный номер', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.short_name + ' ' + self.station.short_name

    class Meta:

        verbose_name = 'Установка'
        verbose_name_plural = 'Установки'

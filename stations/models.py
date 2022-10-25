from django.db import models


# Create your models here.

class Station(models.Model):
    id = models.IntegerField('Ид.', primary_key=True)
    name = models.CharField('Наименование станции', max_length=100)
    short_name = models.CharField('Короткое наименование станции', max_length=10, default='-')
    company = models.CharField('Генерирующая компания', max_length=50, null=True, blank=True)
    address = models.CharField('Адрес нахождения', max_length=100, null=True, blank=True)
    image = models.ImageField('Изображение', blank=True, upload_to='')

    def __str__(self):
        return self.name

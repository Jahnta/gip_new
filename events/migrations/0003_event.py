# Generated by Django 4.0.4 on 2022-11-01 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0002_alter_company_options_alter_station_options_and_more'),
        ('events', '0002_alter_eventtype_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(verbose_name='Дата начала')),
                ('end', models.DateField(verbose_name='Дата окончания')),
                ('duration', models.IntegerField(verbose_name='Длительность')),
                ('event_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.eventtype', verbose_name='Тип события')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stations.unit', verbose_name='Установка')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
    ]

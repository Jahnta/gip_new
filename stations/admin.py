from django.contrib import admin
from .models import Company, Station, Unit
from .models import UnitType

class UnitInLine(admin.TabularInline):
    model = Unit
    extra = 1
    ordering = ('id',)


class StationAdmin(admin.ModelAdmin):
    inlines = [UnitInLine]

admin.site.register(Company)
admin.site.register(Station, StationAdmin)
admin.site.register(Unit)

admin.site.register(UnitType)

# Register your models here.

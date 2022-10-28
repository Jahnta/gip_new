from django.contrib import admin
from .models import Company, Station, Unit
from .models import UnitType

admin.site.register(Company)
admin.site.register(Station)
admin.site.register(Unit)

admin.site.register(UnitType)

# Register your models here.

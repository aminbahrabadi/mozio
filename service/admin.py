from django.contrib.gis import admin
from .models import ServiceArea, Provider

admin.site.register(Provider)
admin.site.register(ServiceArea, admin.GeoModelAdmin)

from django.contrib.gis import admin
from .models import ServiceArea

admin.site.register(ServiceArea, admin.GeoModelAdmin)

from django.contrib.gis import admin
from gistest.models import Place

admin.site.register(Place, admin.OSMGeoAdmin)

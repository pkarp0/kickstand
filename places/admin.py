from django.contrib.gis import admin
from places.models import Place

class PlaceAdmin(admin.OSMGeoAdmin):
    list_display = ('active', 'name', 'address')
    list_display_links = ('name',)
    list_editable = ('active',)

admin.site.register(Place, PlaceAdmin)

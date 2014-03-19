from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from reversegeo.openstreetmap import OpenStreetMap
from gistest.tasks import place_save

class PlaceManager(models.GeoManager):
    def browse(self, lat, lon):
        """return 10 most recent items"""
        items = self.all().order_by('-id')[:10]
        for item in items:
            pass
        return 

class Place(models.Model):
    name = models.CharField(max_length=128)
    coord = models.PointField()
    address = models.TextField(blank=True, null=True)
    objects = PlaceManager()

    def get_absolute_url(self):
        return reverse("place-detail", [self.id,])

    def save(self, *args, **kwargs):
        if len(args) == 0 and kwargs == {}:
            place_save(self)
        else:
            super(models.Model, self).save(*args, **kwargs)            

    def address_from_coord(self, format_string=''):
        ''' use openstreetmap reverse geocoder 
        '''
        g = OpenStreetMap()
        if format_string == '':
            ret = g.reverse(self.coord, default=str(self.coord))
        else:
            ret = g.reverse(self.coord, format_string=format_string)
        return ret
    
    def __unicode__(self):
        return self.name

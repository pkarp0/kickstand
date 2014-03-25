import logging
from math import atan2
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.urlresolvers import reverse
from reversegeo.openstreetmap import OpenStreetMap
from geopy import distance
from gistest.tasks import place_save

logger = logging.getLogger(__name__)

class PlaceManager(models.GeoManager):
    def nearby(self, lat, lon):
        pnt = Point(lon,lat)
        places = Place.objects.filter(coord__distance_lt=(pnt, D(mi=20)) ).distance(pnt).order_by('distance')
        items = []
        for item in places:
            item.distance = item.compute_distance(lat, lon)
            item.orientation = self.orientation(int(item.compute_orientation(lat,lon)))
            items.append(item)
        return items
    
    def browse(self, lat, lon):
        """return 10 most recent items
        and provide distance to each
        """
        places = self.all().order_by('-id')[:10]
        items = []
        for item in places:
            item.distance = item.compute_distance(lat, lon)
            item.orientation = self.orientation(int(item.compute_orientation(lat,lon)))
            items.append(item)
        return items
    
    def orientation(self, degree):
        rotation = [
                    (-180, -157.5, 'W'),
                    (-157.5, -112.5, 'SW'),
                    (-112.5, -67.5, 'S'),
                    (-67.5, -22.5, 'SE'),
                    (-22.5, 22.5, 'E'), 
                    (22.5, 67.5,'NE'), 
                    (67.5, 112.5, 'N'), 
                    (112.5, 157.5, 'NW'),
                    (157.5, 180, 'W'),
                    ]
        for min_deg, max_deg, direction in rotation:
            if degree >= min_deg and degree <= max_deg:
                return direction
        logger.error('degree=%s' % degree)
        return ''
            

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

    def compute_orientation(self, lat, lon):
        ''' orientation around point lat, lon to self '''
        return atan2(self.coord.y - lat, self.coord.x - lon) * 57.2957795 # convert radians to deg

    def compute_distance(self, lat, lon):
        ''' compute distance to lat,lon '''
        point = (lat, lon)
        coord = (coord.y, coord.x)
        return distance.distance(coord, point).miles
        
    def __unicode__(self):
        return self.name

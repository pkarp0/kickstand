from django.contrib.gis.db import models

class PlaceManager(models.GeoManager):
    def browse(self):
        """return 10 most recent items"""
        return self.all().order_by('-id')[:10]

class Place(models.Model):
    name = models.CharField(max_length=128)
    coord = models.PointField()
    objects = PlaceManager()
    
    def __unicode__(self):
        return self.name

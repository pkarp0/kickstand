from django.contrib.gis.db import models

class Place(models.Model):
    name = models.CharField(max_length=128)
    coord = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

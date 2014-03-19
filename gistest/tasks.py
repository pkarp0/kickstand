from django.contrib.gis.db import models

# -- @celery.task(ignore_result=True)
def place_save(place, **kwargs):
    place.address = place.address_from_coord()
    models.Model.save(place)


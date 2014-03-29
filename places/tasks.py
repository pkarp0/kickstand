from __future__ import absolute_import
from django.contrib.gis.db import models

from kickstand.celery import app

@app.task(ignore_result=True)
def place_save(place, **kwargs):
    models.Model.save(place)


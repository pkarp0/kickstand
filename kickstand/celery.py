from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kickstand.settings')

app = Celery('kickstand')
app.config_from_object('kickstand.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from __future__ import absolute_import
from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = 'redis://localhost:6379/1'
CELERY_APP = 'kickstand'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERYD_USER = 'nobody'
CELERYD_GROUP = 'nobody'
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
                       'add-every-3600-seconds': {
                                                  'task': 'kickstand.tasks.add',
                                                  'schedule': timedelta(seconds=3600),
                                                  'args': (16,17)
                                                  },
                       'add-every-monday-morning': {
                                                    'task': 'kickstand.tasks.add',
                                                    'schedule': crontab(hour=7, minute=30, day_of_week=1),
                                                    'args': (10,11)
                                                    }
                       }


from django.conf.urls import patterns, url

urlpatterns = patterns('places.views',
    url(r'^(?P<id>\d+)/$', 'detail', name='place-detail'),
    url(r'^add_nearby/$', 'add_nearby', name='add_nearby'),
    url(r'^nearby/$', 'nearby', name='nearby'),
    )


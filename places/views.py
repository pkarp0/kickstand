from urllib2 import urlopen
import json
import logging
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.gis.geos import Point
from django.conf import settings
from reversegeo.openstreetmap import OpenStreetMap
from places.models import Place, DEFAULT_LAT, DEFAULT_LON
from places.forms import PlaceForm

logger = logging.getLogger(__name__)

def detail(request, id, template='detail.html'):
    item = get_object_or_404(Place, pk=id)
    return render_to_response(
                              template,
                              {'item': item},
                              context_instance = RequestContext( request, {} ),
                              )
RADIUS = 400 #meters
TYPE = 'food'

NEARBY_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?rankby=distance&'
NEARBY_SEARCH_PARAMS = 'types=%(types)s&location=%(lat)s,%(lon)s&sensor=%(sensor)s&key=%(key)s'

def add(request):
    form = PlaceForm(request.POST)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect('/')

def add_nearby(request, template='add.html'):
    if request.method == 'POST':
        return add(request)
    located = request.GET.get('locate', 1)
    try:
        lat = float(request.GET.get('lat', DEFAULT_LAT))
        lon = float(request.GET.get('lon', DEFAULT_LON))
    except (TypeError, ValueError):
        lat = DEAULT_LAT
        lon = DEGAULT_LON
    adict = dict(types=TYPE,
                 lat=lat,
                 lon=lon,
                 radius=RADIUS,
                 sensor="true",
                 key=settings.GOOGLE_APIKEY)
    params = NEARBY_SEARCH_PARAMS % adict
    url = NEARBY_SEARCH + params
    fp = urlopen(url)
    results = json.loads(fp.read())
    logger.debug('params=%s; nearby=%s' % (params, results.get('results', results)))
    address = OpenStreetMap().reverse(Point(lon, lat))

    return render_to_response(template,
                              {'locate': located,
                               'point': address,
                               'nearby' : results['results']},
                              context_instance = RequestContext(request, {})
                              )

def nearby(request):
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        items = Place.objects.nearby(lat, lon)
        located = 1
    except (ValueError, TypeError):
        lat = DEFAULT_LAT
        lon = DEFAULT_LON
        items = Place.objects.browse(lat, lon)
        located = 0
    
    slist = []
    for item in items:
        el = dict(pk=item.pk,
                  name=item.name,
                  coord = str(item.coord),
                  address=item.address,
                  distance=item.distance,
                  orientation=item.orientation
                  )
        slist.append(el)
    items = slist
    address = OpenStreetMap().reverse(Point(lon, lat))
    response_data = {'items': items,
              'point': address, #"POINT(%s %s)" % (lon, lat),
              'located': located,
              'lat': lat,
              'lon': lon
              }
    return HttpResponse(json.dumps(response_data), content_type="application/json")        

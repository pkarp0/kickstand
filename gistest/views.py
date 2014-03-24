from urllib2 import urlopen
import json
import logging
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.gis.geos import Point
from django.conf import settings
from reversegeo.openstreetmap import OpenStreetMap
from gistest.models import Place
from gistest.forms import PlaceForm

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
    return HttpRedirectResponse('/')

def add_nearby(request, template='add.html'):
    if request.method == 'POST':
        return add(request)
        
    lat = float(request.GET.get('lat', 40.67))
    lon = float(request.GET.get('lon', -73.97))
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
                              {'address': address,
                               'nearby' : results['results']},
                              context_instance = RequestContext(request, {})
                              )

def nearby(request, template='nearby.html'):
    lat = float(request.GET.get('lat', 0))
    lon = float(request.GET.get('lon', 0))
    pnt = Point(lon,lat)
    
    items = Place.objects.nearby(lat, lon)
    return render_to_response(template,
                              {'items': items,
                               'lat': lat,
                               'lon': lon
                               },
                              context_instance = RequestContext(request, {})
                              )
    
    
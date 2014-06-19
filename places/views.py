from urllib2 import urlopen
import json
import logging
from django.views.decorators.csrf import csrf_exempt
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
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")        

@csrf_exempt
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
    #results = {}
    #results['results'] = []
    #results['results'].append({u'rating': 3.9, u'name': u'Red Mango', u'reference': u'CnRrAAAARItaYCtdZd62Po36VHf9WW2sTXrG8qpkGmFJnyVwS3_xYmm66KKvKL59syysAoGIAy1tRkJUFunzEDkeJ8Lh8gccNoXAozQFfHlQcbXyvVYtvCtZvFzB4Gq56YFLfNuV0lMGMszK1CEnSiD60puDzhIQ08zZZA2XQo6T9oWr7jT7phoUnn6TeF_Fpat6T_HLyqq74s0BaLY', u'price_level': 1, u'geometry': {u'location': {u'lat': 40.710046, u'lng': -74.006858}}, u'opening_hours': {u'open_now': True}, u'vicinity': u'111 Fulton St, New York', u'photos': [{u'photo_reference': u'CnRnAAAAMneDqmA1W5fpB8vOwrt1-Ly-fsuuxuZtCWMxN5ngw7uefzf79YzD3IPC05F8lK6B-M2AzB6ORt5Yc77YB4Rmp5gCMHoNxmuIwFOtP6Ci6UoL6VJQ7syhdOekVdgq6498XSuc6i9EwUr9AnA8d2F-zhIQREi2vHHfJKrxu_t01i4ulhoU6bdgHg7BVA4GTc6Izag2luyHycA', u'width': 960, u'html_attributions': [], u'height': 720}], u'id': u'a5ce3c08a46daf1288702fac7be858ae3504d550', u'types': [u'store', u'restaurant', u'food', u'establishment'], u'icon': u'http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png'})
    #results['results'].append({u'rating': 3.9, u'name': u'Green Mango', u'reference': u'CnRrAAAARItaYCtdZd62Po36VHf9WW2sTXrG8qpkGmFJnyVwS3_xYmm66KKvKL59syysAoGIAy1tRkJUFunzEDkeJ8Lh8gccNoXAozQFfHlQcbXyvVYtvCtZvFzB4Gq56YFLfNuV0lMGMszK1CEnSiD60puDzhIQ08zZZA2XQo6T9oWr7jT7phoUnn6TeF_Fpat6T_HLyqq74s0BaLY', u'price_level': 1, u'geometry': {u'location': {u'lat': 40.710046, u'lng': -74.006858}}, u'opening_hours': {u'open_now': True}, u'vicinity': u'111 Fulton St, New York', u'photos': [{u'photo_reference': u'CnRnAAAAMneDqmA1W5fpB8vOwrt1-Ly-fsuuxuZtCWMxN5ngw7uefzf79YzD3IPC05F8lK6B-M2AzB6ORt5Yc77YB4Rmp5gCMHoNxmuIwFOtP6Ci6UoL6VJQ7syhdOekVdgq6498XSuc6i9EwUr9AnA8d2F-zhIQREi2vHHfJKrxu_t01i4ulhoU6bdgHg7BVA4GTc6Izag2luyHycA', u'width': 960, u'html_attributions': [], u'height': 720}], u'id': u'a5ce3c08a46daf1288702fac7be858ae3504d550', u'types': [u'store', u'restaurant', u'food', u'establishment'], u'icon': u'http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png'})
    logger.debug('params=%s; nearby=%s' % (params, results.get('results', results)))
    address = OpenStreetMap().reverse(Point(lon, lat))
    # add a none of the above choice
    nota = {u'rating': 0.0, u'name': u'None of the above', u'reference': '', u'price_level': 1, u'geometry': {u'location': {u'lat': lat, u'lng': lon}}, u'opening_hours': {u'open_now': True}, u'vicinity': address, u'photos': [{u'photo_reference': u'', u'width': 0, u'html_attributions': [], u'height': 0}], u'id': u'', u'types': [u'store', u'restaurant', u'food', u'establishment'], u'icon': u''}
    # results['results'].append(nota)
    response_data = {'locate': located,
                     'point': address,
                     'items' : results['results']},
    return HttpResponse(json.dumps(response_data), content_type="application/json")        

def nearby(request):
    try:
        dist = float(request.GET.get('dist', 1.0))
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        items = Place.objects.nearby(lat, lon, dist)
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
                  lng = item.coord.x,
                  lat = item.coord.y,
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

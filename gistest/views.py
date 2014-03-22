from urllib2 import urlopen
import json
import logging
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.conf import settings

from gistest.models import Place

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
NEARBY_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
NEARBY_SEARCH_PARAMS = 'type=%(type)s&location=%(lat)s,%(lon)s&radius=%(radius)s&sensor=%(sensor)s&key=%(key)s'

def nearby(request, template='nearby.html'):
    lat = request.GET.get('lat', 0)
    lon = request.GET.get('lon', 0)
    adict = dict(type=TYPE,
                 lat=lat,
                 lon=lon,
                 radius=RADIUS,
                 sensor="true",
                 key=settings.GOOGLE_APIKEY)
    params = NEARBY_SEARCH_PARAMS % adict
    url = NEARBY_SEARCH + params
    fp = urlopen(url)
    results = json.loads(fp.read())
    logger.debug('nearby=%s' % results)
    return render_to_response(template,
                              {'nearby' : results},
                              context_instance = RequestContext(request, {})
                              )
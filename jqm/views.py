import logging
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from reversegeo.openstreetmap import OpenStreetMap
from places.models import Place, DEFAULT_LAT, DEFAULT_LON
from jqm.forms import RegistrationForm
from django.contrib.gis.geos import Point

logger = logging.getLogger(__name__)
def home( request, template='jqm/main.html' ):
    ''' use users lat/lon to show distance to places '''
    located = request.GET.get('locate', 1)
    try:
        lat = float(request.GET.get('lat', DEFAULT_LAT))
        lon = float(request.GET.get('lon', DEFAULT_LON))
        #items = Place.objects.nearby(lat, lon)

    except (TypeError, ValueError):
        logger.error('user=%s; lat=%s' % (request.user, lat))
        lat = DEFAULT_LAT
        lon = DEFAULT_LON
        #items = Place.objects.browse(lat, lon)

    logger.debug('user=%s; lat=%s; lon=%s' % (request.user, lat, lon))
    address = OpenStreetMap().reverse(Point(lon, lat))
    
    return render_to_response(
        template,
        {
         'point': address, #"POINT(%s %s)" % (lon, lat),
         'locate': located,
         'lat': lat,
         'lon': lon
         },
        context_instance = RequestContext( request, {} ),
    )

@csrf_protect
def register(request):
    if request.method == 'POST':
        print request.POST
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
        else:
            print form
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'jqm/registration/registration.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'jqm/registration/success.html',
    )

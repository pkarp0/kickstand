import logging
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from reversegeo.openstreetmap import OpenStreetMap
from places.models import Place
from jqm.forms import RegistrationForm
from django.contrib.gis.geos import Point

logger = logging.getLogger(__name__)
def home( request, template='jqm/index.html' ):
    ''' use users lat/lon to show distance to places '''
    located = request.GET.get('locate', 1)
    try:
        lat = float(request.GET.get('lat', 40.67))
    except ValueError:
        logger.error('user=%s; lat=%s' % (request.user, lat))
        lat = 40.97
    try:
        lon = float(request.GET.get('lon', -73.97))
    except ValueError:
        logger.error('user=%s; lon=%s' % (request.user, lon))
        lon = -73.97
    logger.debug('user=%s; lat=%s; lon=%s' % (request.user, lat, lon))
    address = OpenStreetMap().reverse(Point(lon, lat))
    return render_to_response(
        template,
        {'items': Place.objects.browse(lat, lon),
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

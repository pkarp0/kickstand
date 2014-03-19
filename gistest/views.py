from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext

from gistest.models import Place

def detail(request, id, template='detail.html'):
    item = get_object_or_404(Place, pk=id)
    return render_to_response(
                              template,
                              {'item': item},
                              context_instance = RequestContext( request, {} ),
                              )

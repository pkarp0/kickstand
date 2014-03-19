
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext

from gistest.models import Place
from jqm.forms import RegistrationForm

def home( request ):
    return render_to_response(
        'jqm/index.html',
        {'items': Place.objects.browse()},
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

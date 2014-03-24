from django.forms import ModelForm
from gistest.models import Place

class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'address', 'coord']

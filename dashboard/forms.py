
from django.forms import ModelForm
from .models import GettingLocations

class GettingLocationForM(ModelForm):
    class Meta:
        model = GettingLocations       
 
        # Custom fields
        fields =["startingPoint", "destinationPoint"]

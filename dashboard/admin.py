from django.contrib import admin
from .models import Locations,Location_Order,Statics_Searching,Infromations_related_to_a_tour
admin.site.register(Locations)
admin.site.register(Location_Order)
admin.site.register(Statics_Searching)
admin.site.register(Infromations_related_to_a_tour)
# Register your models here.

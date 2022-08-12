
from django.db import models
from django.forms import CharField, ModelForm
from webhook.models import Buses,Turn_of_bus

class Locations(models.Model):
    name = models.CharField(max_length=1000)
    route_number = models.CharField(max_length=100)
    geographic_location = models.CharField(max_length=100)
    sub_route = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(f"{self.name} - {self.route_number}")

class GettingLocations(models.Model):
    tuple_of_locations = []

    def __init__(self):
        locations = Locations.objects.all()
        for location in locations:
            self.tuple_of_locations.append((location.name,location.name))
        self.tuple_of_locations = tuple(self.tuple_of_locations)
        print(self.tuple_of_locations)
    
    startingPoint = models.CharField(choices=tuple_of_locations,max_length=200)
    destinationPoint = models.CharField(choices=tuple_of_locations,max_length=200)
        
class Location_Order(models.Model):
    route_number = models.IntegerField()
    sub_route = models.IntegerField(default=0)
    list_of_locations = models.CharField(max_length=10000)

    def __str__(self):
        return self.list_of_locations
        

class Statics_Searching(models.Model):
    key_id = models.AutoField(primary_key=True)
    bus_id = models.CharField(max_length=50)
    destination_point = models.CharField(max_length=300)
    starting_point = models.CharField(max_length=200)
    user_location = models.CharField(max_length=200)
    starting_point_to_destination_point = models.BooleanField()
    route_number = models.IntegerField()
    startcoordinates = models.CharField(max_length=100,default="False")
    endcoordinates = models.CharField(max_length=100,default="False")
    needdirections = models.BooleanField(default=False)
    how_much_of_time = models.CharField(max_length=100,default="o mins")
    times_of_shedules = models.CharField(max_length=100,default="")
    def __str__(self):
        return f'{self.route_number} - {self.key_id}'

class Infromations_related_to_a_tour(models.Model):
    tour_id = models.ForeignKey('Statics_Searching',on_delete=models.CASCADE)
    google_api_time_estimation = models.CharField(max_length=100)
    number_of_times_requested = models.IntegerField(default=0)

    def __str__(self):
        return f"Tour - {self.tour_id}"
    def __init__(self,location_of_user,location_of_bus_stop,bus_id,tour_id,nearest_location):
        relevent_bus = Buses.objects.get(bus_registration_number= bus_id)
        current_turn_of_bus = Turn_of_bus.objects.get(bus_id=relevent_bus)
        bus_current_location = f"{current_turn_of_bus.current_altitude},{current_turn_of_bus.current_longitude}"
        name_location_of_user = Statics_Searching.objects.get(pk=tour_id).starting_point
        geo_location_of_user = Locations.objects.get(name=name_location_of_user).geographic_location
        
        # all_locations = Locations.objects.values_list('name','geographic_location')
        # geo_all_locations = (str(Location_Order.objects.get(route_number=relevent_bus.route_number).list_of_locations)).split(",")
        # index_of_user_location = geo_all_locations.index(name_location_of_user)
        # index_of_bus_location = geo_all_locations.index(nearest_location)
        # if index_of_user_location > index_of_bus_location :
        #     for i in range(index_of_bus_location,index_of_user_location,5):
        #         list_of_geo_locations = all_locations[i]
        #         print(i)




from django.db import models
from django.forms import CharField, ModelForm

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
    destination_point = models.CharField(max_length=300)
    starting_point = models.CharField(max_length=200)
    user_location = models.CharField(max_length=200)
    starting_point_to_destination_point = models.BooleanField()
    route_number = models.IntegerField()

    def __str__(self):
        return f'{self.route_number} - {self.key_id}'

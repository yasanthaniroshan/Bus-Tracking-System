from pyexpat import model
from django.db import models


class Buses(models.Model):
    bus_registration_number = models.CharField(max_length=32)
    route_number = models.IntegerField()
    sub_route_numer = models.IntegerField(default=0)
    destination = models.CharField(max_length=100)
    starting_point = models.CharField(max_length=100)
     
    def __str__(self):
        return f"{self.bus_registration_number} | {self.route_number}/{self.sub_route_numer} - [{self.destination} -> {self.starting_point}]"


class Turn_of_bus(models.Model):
    bus_id = models.ForeignKey('Buses', on_delete=models.CASCADE)
    current_time = models.TimeField()
    last_location = models.CharField(max_length=100)
    next_location = models.CharField(max_length=100)
    current_longitude = models.FloatField()
    current_altitude = models.FloatField()
    started = models.BooleanField()
    starting_time = models.TimeField()
   

class Shedule(models.Model):
    bus_id = models.ForeignKey('Buses',on_delete=models.CASCADE)
    destinaton_to_starting_point = models.CharField(max_length=1000)
    starting_point_to_destination = models.CharField(max_length=1000)
    times_of_turns = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.bus_id)

    

class Active_buses(models.Model):
    bus_id = models.ForeignKey('Buses',on_delete=models.CASCADE)
    active = models.BooleanField()
    active_time = models.TimeField()
    starting_time = models.CharField(max_length=100)
    def __str__(self):
        return str(self.bus_id)


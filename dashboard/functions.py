
from time import localtime
from unicodedata import name
from webhook.views import time_calculater,googledistance
from webhook.models import Buses,Shedule
from .models import Location_Order,Locations, Statics_Searching
from geopy import distance

def distance_Calc(coords_1,coords_2): 
    
    distance_varivle = str(distance.distance(coords_1, coords_2)).split(".")
    if (distance_varivle[1][-6:-5] == "-"):
        strings = "0.00"
    else:
        strings = distance_varivle[0]+ "."+ str(distance_varivle[1])[:4]
    return round(float(strings),2)

def getextractlocation(starting_point,destination_point):
    data_to_pass ={}
    location_ordered_list =[]
    distance_list = []
    distance_list_names = []
    startingpointtodestination=''
    if "," in destination_point:
        locations = Locations.objects.get(name=starting_point)
        route_number = int(locations.route_number)
        latitude,longitude = destination_point.split(",")
        coordinates = (float(latitude),float(longitude))
        all_locations = Locations.objects.all()

        for location in all_locations:
            currenT_coordinates = location.geographic_location
            
            latitude,longitude = currenT_coordinates.split(",")
            currenT_coordinates = (float(latitude),float(longitude))
            
            distance_list.append(float(distance_Calc(coordinates,currenT_coordinates)))
        
            distance_list_names.append(location.name)

        
        distance_list_unsoted = [x for x in distance_list]
        distance_list.sort()
    
        nearest_location_1 = distance_list_names[distance_list_unsoted.index(distance_list[0])]
        nearest_location_2 = distance_list_names[distance_list_unsoted.index(distance_list[1])]

        print(nearest_location_1)
        print(nearest_location_2)

        locations_order_object = Location_Order.objects.get(route_number=route_number).list_of_locations.split(",")
        startcoordinates = Locations.objects.get(name=nearest_location_1).geographic_location
        endcoordinates = destination_point
        if(locations_order_object.index(nearest_location_1)>locations_order_object.index(starting_point)):
            startingpointtodestination = True
        else:
            startingpointtodestination = False

        data_to_pass = {"destination_point":nearest_location_1,"starting_point":starting_point,"userlocation":starting_point,"startingpointtodestination":startingpointtodestination,"route_number":route_number,"startcoordinates":startcoordinates,"endcoordinates":endcoordinates,"needdirections":True}

        return data_to_pass
    elif "," in starting_point:
        locations = Locations.objects.get(name=destination_point)
        route_number = int(locations.route_number)
        latitude,longitude = starting_point.split(",")
        coordinates = (float(latitude),float(longitude))
        all_locations = Locations.objects.all()

        for location in all_locations:
            currenT_coordinates = location.geographic_location
            
            latitude,longitude = currenT_coordinates.split(",")
            currenT_coordinates = (float(latitude),float(longitude))
            
            distance_list.append(float(distance_Calc(coordinates,currenT_coordinates)))
        
            distance_list_names.append(location.name)
        
        distance_list_unsoted = [x for x in distance_list]
        distance_list.sort()
    
        nearest_location_1 = distance_list_names[distance_list_unsoted.index(distance_list[0])]
        nearest_location_2 = distance_list_names[distance_list_unsoted.index(distance_list[1])]
        
       
        print(nearest_location_1)
        print(nearest_location_2)

        locations_order_object = Location_Order.objects.get(route_number=route_number).list_of_locations.split(",")
        startcoordinates = starting_point
        endcoordinates = Locations.objects.get(name= nearest_location_1).geographic_location
        if(locations_order_object.index(nearest_location_1)>locations_order_object.index(destination_point)):
            startingpointtodestination = False
        else:
            startingpointtodestination =True

        data_to_pass = {"destination_point":destination_point,"starting_point":nearest_location_1,"userlocation":starting_point,"startingpointtodestination":startingpointtodestination,"route_number":route_number,"startcoordinates":startcoordinates,"endcoordinates":endcoordinates,"needdirections":True}
        
        return data_to_pass

    else:
        locations = Locations.objects.get(name=starting_point)
        route_number = int(locations.route_number)

        locations_order_object = Location_Order.objects.get(route_number=route_number).list_of_locations.split(",")
        
        if(locations_order_object.index(starting_point)>locations_order_object.index(destination_point)):
            startingpointtodestination = False
        else:
            startingpointtodestination =True

        data_to_pass = {"destination_point":destination_point,"starting_point":starting_point,"userlocation":starting_point,"startingpointtodestination":startingpointtodestination,"route_number":route_number,"startcoordinates":"False","endcoordinates":"False","needdirections":False}
        
        return data_to_pass

    
    # location_order_object =Location_Order.objects.get(route_number=route_number)

    # for location in location_order_object:
    #     location_ordered_list.append(location.name)
def finding_nearest_shedule(route_number,startingpointtodestination):
    dict_of_shedule_times = {}
    list_of_values =[]
    list_of_values_sorted = []
    all_buses_with_route_number = Buses.objects.filter(route_number=route_number)
   
    if startingpointtodestination == True:
        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
            for time in starting_to_destination:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x)  for x in list_of_values]
        list_of_values_sorted.sort()
        nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]

    elif startingpointtodestination == False:

        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            destinaton_to_starting_point = str(bus_shedule.destinaton_to_starting_point).split(',')
            for time in destinaton_to_starting_point:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x)  for x in list_of_values]
        list_of_values_sorted.sort()
        nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]

    return nearest_time_and_bus



def finding_how_many_available_times(route_number,startingpointtodestination,key_id):
    dict_of_shedule_times = {}
    list_of_values =[]
    list_of_values_sorted = []
    available_shedules = {}
    all_buses_with_route_number = Buses.objects.filter(route_number=route_number)
    
    
    
    user_location = Statics_Searching.objects.get(key_id=key_id).starting_point
    geolocation = Locations.objects.get(name=user_location).geographic_location

    if startingpointtodestination == True:


        bus_starting_point = Buses.objects.get(route_number=route_number).starting_point
        
        time_for_tour = googledistance(bus_starting_point,geolocation)
        print(time_for_tour)
        time_in_seconds = 3600*int(time_for_tour["hours"])+60*int(time_for_tour["minutes"])

        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
            for time in starting_to_destination:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x) for x in list_of_values if int(x) > time_in_seconds]
        list_of_values_sorted.sort()
        nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]
        for shedule in list_of_values_sorted:
            
            # details = ''
            # details = str(dict_of_shedule_times[shedule]).split('/')
        
            # data = {"bus-id":details[0],"time":details[1]}
            # print(type(data))
            available_shedules.update({f"{list_of_values_sorted.index(shedule)}":f"{dict_of_shedule_times[shedule]}"})
        
        
    elif startingpointtodestination == False:

        bus_starting_point = Buses.objects.get(route_number=route_number).destination

        time_for_tour = googledistance(bus_starting_point,geolocation)
        print(time_for_tour)
        time_in_seconds = 3600*int(time_for_tour["hours"])+60*int(time_for_tour["minutes"])

        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            destinaton_to_starting_point = str(bus_shedule.destinaton_to_starting_point).split(',')
            for time in destinaton_to_starting_point:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x)  for x in list_of_values if int(x) > time_in_seconds]
        list_of_values_sorted.sort()
        nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]
        for shedule in list_of_values_sorted:
             
            # details = ''
            # details = str(dict_of_shedule_times[shedule]).split('/')
        
            # data = {"bus-id":details[0],"time":details[1]}
            # print(type(data))
            available_shedules.update({f"{list_of_values_sorted.index(shedule)}":f"{dict_of_shedule_times[shedule]}"})
    return available_shedules

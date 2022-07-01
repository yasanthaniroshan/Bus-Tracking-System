
from posixpath import split
from .models import Buses,Shedule
from datetime import datetime
import pytz
from dashboard.models import Locations,Location_Order
from geopy import distance
distance_between_nearest_locations = []
next_and_last = {}
def distance_Calc(coords_1,coords_2): 
    
    distance_varivle = str(distance.distance(coords_1, coords_2)).split(".")
    if (distance_varivle[1][-6:-5] == "-"):
        strings = "0.00"
    else:
        strings = distance_varivle[0]+ "."+ str(distance_varivle[1])[:4]
    return round(float(strings),2)

TIME_ZONE = 'Asia/Kolkata'


def time_calculater_for_js(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = abs(total_seconds_data - total_seconds_now)
    
    return time_difference

def finding_nearest_shedule(bus_id):
    dict_of_shedule_times = {}
    list_of_values =[]
    list_of_values_sorted = []
    all_buses_with_route_number = Buses.objects.filter(bus_registration_number=bus_id)
    
    
    for bus in all_buses_with_route_number:
        bus_shedule = Shedule.objects.get(bus_id = bus)
        starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
        for time in starting_to_destination:
            dict_of_shedule_times.update({time_calculater_for_js(time):f"{bus.bus_registration_number}/{time}/1"})
        destinaton_to_starting_point = str(bus_shedule.destinaton_to_starting_point).split(',')
        for time in destinaton_to_starting_point:
            dict_of_shedule_times.update({time_calculater_for_js(time):f"{bus.bus_registration_number}/{time}/0"})
    
    list_of_values = list(dict_of_shedule_times.keys())
    list_of_values_sorted = [int(x)  for x in list_of_values]
    list_of_values_sorted.sort()
  
    nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]
    differance = list_of_values_sorted[0]
    time_travel = nearest_time_and_bus.split("/")
    print("nearest sheduled time ",time_travel[1])
    return f"{nearest_time_and_bus}/{differance}"

def find_last_and_next_locations(coordinates,route_number):
   
    distance_list = []
    distance_list_names = []
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

    locations_order_object = Location_Order.objects.get(route_number=route_number).list_of_locations.split(",")
    index_of_nearest_location = locations_order_object.index(nearest_location_1)
   
    if index_of_nearest_location == 0 :
        before_location = locations_order_object[0]
        next_location = locations_order_object[2] 
    elif index_of_nearest_location == 44:
        next_location = locations_order_object[44]
        before_location = locations_order_object[42]
    else:
        before_location = locations_order_object[index_of_nearest_location - 1]
        next_location = locations_order_object[index_of_nearest_location + 1]
    
    location_before = {"name":before_location,"distance":distance_list_unsoted[locations_order_object.index(before_location)]}
    location_next = { "name":next_location,"distance":distance_list_unsoted[locations_order_object.index(next_location)]}
    current_location = {"name":nearest_location_1,"distance":distance_list[0]}
    location_two = {"location_before":location_before,"location_next":location_next,"location":current_location}
    distance_between_nearest_locations.append(location_two)
    print("nearest bus stand :",current_location)
    
    if len(distance_between_nearest_locations)>4:
        last_data_location_before = distance_between_nearest_locations[0]["location_before"]["distance"]
        last_data_location_next = distance_between_nearest_locations[0]["location_next"]["distance"]
        new_data_location_before = distance_between_nearest_locations[3]["location_before"]["distance"]
        new_data_location_next = distance_between_nearest_locations[3]["location_next"]["distance"]
        last_current_location = distance_between_nearest_locations[0]["location"]["distance"]
        new_data_current_location = distance_between_nearest_locations[3]["location"]["distance"]

        if last_current_location < new_data_current_location :
            next_and_last.update({"next_location":distance_between_nearest_locations[0]["location"]["name"],"last_location":distance_between_nearest_locations[0]["location_before"]["name"],"Started":True})
        elif new_data_current_location < last_current_location :
            next_and_last.update({"next_location":distance_between_nearest_locations[0]["location_next"]["name"],"last_location":distance_between_nearest_locations[0]["location"]["name"],"Started":True})
        else:
            next_and_last.update({"next_location":"Not -Yet startted","last_location":"Not -Yet startted","Started":False})
        distance_between_nearest_locations.pop(0)
        
    return next_and_last
    
   
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import geopy.distance
import requests
from .models import Buses, Shedule,Active_buses, Turn_of_bus
import pytz,json
from datetime import datetime
import json
from .functions import finding_nearest_shedule,find_last_and_next_locations
from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import Infromations_related_to_a_tour,Locations, Statics_Searching

TIME_ZONE = 'Asia/Kolkata'

last_records_location = []

mode = "DRIVING"
key = "AIzaSyAZdDhFvl1DzEL8yLQ4EyHPF11nxJyUKF4"


payload={}
headers = {}

def googledistance(startingpoint,userlocation):
    if startingpoint == "Not -Yet startted":
        return {"hours":0,"minutes":0}
    origin = Locations.objects.get(name=startingpoint).geographic_location
    destination = userlocation
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&alternatives=false&avoid=tolls&key={key}"
    response = requests.request("GET", url, headers=headers, data=payload)
    jsoned_data = json.loads(response.text)
    duration =  jsoned_data["routes"][0]["legs"][0]["duration"]["text"]
    list_duration = duration.split(" ")
    if len(list_duration) == 2:
        hours = 0
        minutes = list_duration[0]
    elif len(list_duration) == 4:
        hours = list_duration[0]
        minutes = list_duration[2]
    return {"hours":hours,"minutes":minutes}


def time_calculater(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = total_seconds_data - total_seconds_now
    if time_difference < 0:
        time_difference = 86400 - total_seconds_now +total_seconds_data
    return time_difference


def time_calculater_for_js(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = total_seconds_data - total_seconds_now
    
    return abs( time_difference)
def time_calculater_for_started(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = total_seconds_data - total_seconds_now
    
    return  time_difference


def distance_Calc(coords_1,coords_2): 
    
    distance = str(geopy.distance.distance(coords_1, coords_2)).split(".")
    if (distance[1][-6:-5] == "-"):
        strings = "0.00"
    else:
        strings = distance[0]+ "."+ str(distance[1])[:2]
    return round(float(strings),2)
 


@csrf_exempt
def ActiveOrDisconnected(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bus_id = data['bus_id']
        tour_id = data['tour_id'][:-1]
        print("javascript data recieved :",bus_id)
    # informations_of_tour = Infromations_related_to_a_tour.objects.get(tour_id=tour_id)
    statics_of_tour = Statics_Searching.objects.get(pk=tour_id).starting_point
    relevent_bus = Buses.objects.get(bus_registration_number=bus_id)
    current_bus = Active_buses.objects.get(bus_id=relevent_bus)
    last_active_time = current_bus.active_time
    differance = time_calculater_for_js(last_active_time)
    if differance < 60 :
        time_for_live = f"{differance} Seconds ago"
    elif differance > 59 and differance < 3600 :
        time_for_live = f"{round(differance/60)} Minutes ago"
    elif differance > 3599 :
        time_for_live = f"{round(differance/3600)} Hours ago"
    print(time_for_live)
    render_data = {}
    
    if differance > 1200:
        current_bus.active = False
        current_bus.save()
        render_data['connected'] = "false"
    else:
        current_bus.active = True
        current_bus.save()
        render_data['connected'] = "true"
    geo_location = Locations.objects.get(name=statics_of_tour).geographic_location
    
    current_details = Turn_of_bus.objects.filter(bus_id=relevent_bus).order_by('current_time')[0]
    started_difference = time_calculater_for_started(current_bus.starting_time)
    if started_difference > 0:
        render_data["started"] = "false"
        current_details.started = False
    else:
        render_data["started"] = "true"
        current_details.started = True
    

    print("Started or not",render_data["started"])
    time_remaining = googledistance(current_details.next_location,geo_location)
    render_data["times_ago"] = time_for_live
    render_data["last_location"] = current_details.last_location
    render_data["next_location"] = current_details.next_location
    render_data["current_longitude"] = current_details.current_longitude
    render_data["current_altitude"] = current_details.current_altitude
   
    render_data["bus_stand"] = geo_location
    render_data["hours_free"] = time_remaining["hours"]
    render_data["minutes_free"] = time_remaining["minutes"]
    current_details.save()
    print(render_data)
    
    return JsonResponse(render_data,headers={"access-control-allow-origin" : "*", 
"access-control-allow-credentials" : "true"})
    


@csrf_exempt
def iotdevice(request):
    if request.method == 'POST':
        turn_bus_records = Turn_of_bus()
        bus_id = request.headers["id"]
        bus_route = request.headers["route"]
        connected_status = request.headers["connected"]
        json_converted = json.load(request)
        location = ((json_converted["altitude"]),(json_converted["longitude"]))
        print(f"My ID - {bus_id} | message - '{json_converted['massage']}'")
        relevent_bus = Buses.objects.get(bus_registration_number = bus_id)
        activeordisconected = Active_buses.objects.get(bus_id=relevent_bus)
        activeordisconected.active = True
        activeordisconected.active_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
        details = finding_nearest_shedule(bus_id)
            
        registration_number,time,start_to_end,difference = str(details).split("/")
        
        print(f"my current location - {location} | connected {connected_status}")
        try:
            current_turn = Turn_of_bus.objects.get(bus_id=relevent_bus)
        except ObjectDoesNotExist:
            current_turn = Turn_of_bus.objects.create(
                bus_id = relevent_bus,
                current_altitude = 0,
                current_longitude = 0,
                starting_time = "00:00",
                next_location = "none",
                last_location = "None",
                started = False,
                current_time =  datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S"),
            )
        activeordisconected.starting_time = time
        current_turn = Turn_of_bus.objects.filter(bus_id=relevent_bus).order_by('current_time')[0]
        activeordisconected.save()
        last_records_location.append(location)
        data_about_locations =  find_last_and_next_locations(location,bus_route)
        current_turn.bus_id = relevent_bus
        current_turn.current_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
        if len(last_records_location)> 4:
            current_turn.current_altitude = json_converted["altitude"]
            current_turn.current_longitude = json_converted["longitude"]
            current_turn.starting_time = activeordisconected.starting_time
            current_turn.next_location = data_about_locations["next_location"]
            current_turn.last_location = data_about_locations["last_location"]
            current_turn.started = data_about_locations["Started"]
            current_turn.save()        
        if(len(last_records_location)>4):
            distance = float(distance_Calc(last_records_location[len(last_records_location) - 4],location))
              
            if distance < 0.5 :
                last_records_location.pop(0)

        return HttpResponse("Webhook received!")

    if request.method == "GET":
        bus_id = request.headers["id"]
        responce_for_time = ''
        relevent_bus = Buses.objects.get(bus_registration_number = bus_id)
        print(relevent_bus.id)
        bus_shedule = Shedule.objects.get(bus_id=relevent_bus)
        bus_destination_to_starting = str(bus_shedule.destinaton_to_starting_point).split(',')
        bus_starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
        all_shedules = {}
        for times in bus_destination_to_starting:
            all_shedules.update({times : time_calculater(times)})
        for times in bus_starting_to_destination:
            all_shedules.update({times : time_calculater(times)})
        data_values =list(int(x) for x in all_shedules.values())
        data_values.sort()
        
        time_in_seconds = data_values[0]
        data_keys = list(all_shedules.keys())

        data_values = list(int(x) for x in all_shedules.values())
        data_to_send_server = data_keys[data_values.index(time_in_seconds)]
        print(bus_id,data_to_send_server)
        activeordisconected = Active_buses.objects.get(bus_id=relevent_bus)
        activeordisconected.active = True
        activeordisconected.active_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
        activeordisconected.starting_time = data_to_send_server
        activeordisconected.save()
        return HttpResponse(data_to_send_server)



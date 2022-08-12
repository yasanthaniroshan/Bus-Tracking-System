from ast import List
from multiprocessing import context
from django.shortcuts import redirect, render
from webhook.models import Buses,Active_buses,Turn_of_bus
from .functions import getextractlocation,finding_nearest_shedule,finding_how_many_available_times
from django.http import HttpResponseRedirect

from .models import Locations,Statics_Searching


def extract_location(extractlocation):
    if extractlocation == None:
        return redirect('location')
    else:
        destination = extractlocation["destination_point"]
        starting = extractlocation["starting_point"]
        user_location = extractlocation["userlocation"]
        start_to_destination = extractlocation["startingpointtodestination"]

def tourdetails(request,tour_id_with_number):
    tour_id = str(tour_id_with_number)[:-1]
    tour_id = int(tour_id)
    tourdetails_object = Statics_Searching.objects.get(pk=tour_id)
    bus_and_time = finding_nearest_shedule(tourdetails_object.route_number,tourdetails_object.starting_point_to_destination_point)
    bus_id,time = bus_and_time.split("/")
    print("nearest time",time)
    
    relevent_bus = Buses.objects.get(bus_registration_number=bus_id)
    locations = Turn_of_bus.objects.filter(bus_id=relevent_bus).order_by('current_time')[0]
    print(locations.last_location)
    print(5*"------")
    available_times = finding_how_many_available_times(tourdetails_object.route_number,tourdetails_object.starting_point_to_destination_point,tour_id)
    print(available_times)
    print(5*"------")
    context = {"bus":relevent_bus,"tour_details":tourdetails_object,"time":time,"locations":locations}
    return render(request,'tourdetails.html',context)

def tourdashboard(request,bus_id):
    buses = Buses()
    relevent_bus = Buses.objects.get(bus_registration_number=bus_id)
    active_bus = Active_buses.objects.get(pk=relevent_bus.id)
    turn_of_bus = Turn_of_bus.objects.get(pk=relevent_bus.id) 
  

    context = {"bus_details":relevent_bus,"bus_status":active_bus,"turn_of_bus":turn_of_bus}
    print(relevent_bus.bus_registration_number)
    return render(request,"dashboard.html",context)
    
def frontpage(request):
    return render(request,'frontpage.html')

def gettinglocations(request):
    getting_data = Locations.objects.all()
    if request.method == "POST":
        starting_point = request.POST['startingpoint']
        destination_point = request.POST['destinationpoint']
        
        print("Starting Point :",starting_point)
        print("destination Point :",destination_point)
       
        extract_location = getextractlocation(starting_point,destination_point)
        new_data = Statics_Searching()
        new_data.starting_point = extract_location["starting_point"]
        new_data.destination_point = extract_location["destination_point"]
        new_data.starting_point_to_destination_point = extract_location["startingpointtodestination"]
        new_data.route_number = extract_location["route_number"]
        new_data.user_location = extract_location["userlocation"]
        new_data.startcoordinates = extract_location["startcoordinates"]
        new_data.endcoordinates = extract_location["endcoordinates"]
        new_data.needdirections = extract_location["needdirections"]
        new_data.save()
        return redirect('available-shedules',new_data.key_id)

    else:
        print("data not valid")
    
    return render(request,'locations.html',{"form":getting_data})


def survey(request):
    return render(request,'survey.html')

def avaialableshedules(request,tour_id):
    tourdetails_object = Statics_Searching.objects.get(pk=tour_id)
    print(5*"------")
    context = []
    times = ""
    
    available_times = finding_how_many_available_times(tourdetails_object.route_number,tourdetails_object.starting_point_to_destination_point,tour_id)
    data = available_times
    for time_shedule in data:
        
        bus_id,time = data[time_shedule].split("/")
        times = times + "," + time
        bus = Buses.objects.get(bus_registration_number=bus_id)
        
        context.append({"url_slug":f"{tour_id}{time_shedule}","bus_id":bus_id,"startingpoint":f"{bus.starting_point}","destination":f"{bus.destination}","time":time})
    
    print(times)

    print(5*"------")
    tourdetails_object.times_of_shedules = times[1:]
    tourdetails_object.save()
    return render(request,'shedules.html',{"data":context,"key_id":tour_id})
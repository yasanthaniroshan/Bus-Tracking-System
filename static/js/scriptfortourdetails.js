
let path = location.pathname;
let directories = path.split("/");
let tour_id = directories[(directories.length - 1)];
let online_or_offline = document.getElementById("live_text");
let last_location = document.getElementById("last_location");
let next_location = document.getElementById("next_location");
let bus_id = document.getElementById("bus_id").textContent;
const sheduled = document.getElementById("sheduled");
const sheduled_text = document.getElementById("sheduled-text");
const time_live = document.getElementById("live-time");
let longitude = 0;
let latitude = 0;
let device_latitude = 0;
let device_longitude = 0;
const bus_stop = document.getElementById("starting-point-name");
let data_f;
let times = 0;
const hours_free = document.getElementById("hours-free");
const minutes_free = document.getElementById("minutes-free");

const url = "https://finnc.herokuapp.com/api/js/";

const icon = "https://finnc.herokuapp.com/static/images/tourdetails/bus-stop.png";




function getLocation() {
    let pos;
    navigator.geolocation.getCurrentPosition(
        (position) => {
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
            pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
        })
    console.log("latitude : ", latitude);
    console.log("longtitude : ", longitude);

    return pos;

};

function dataToSend() {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
        })
    let data = {
        'bus_id': bus_id,
        "latitude": latitude,
        "longtitude": longitude,
        "tour_id": tour_id,
    }
    return data;
}

let location_of_me = getLocation();
let location_of_bus = { lat: device_latitude, lng: device_longitude };

const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: location_of_me,
});

// const marker_of_me = new google.maps.Marker({
//     position: location_of_me,
//     map: map,
// });

const marker_of_bus = new google.maps.Marker({
    position: location_of_bus,
    map: map,
    icon: icon,
});

function calcRoute(bus_lat,bus_lng,device_latitude,device_longitude) {
    var start = new google.maps.LatLng(device_latitude,device_longitude);
    var end = new google.maps.LatLng(bus_lat,bus_lng);
    var directionsService = new google.maps.DirectionsService();
    var directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    var request = {
      origin: start,
      destination: end,
      travelMode: 'WALKING'
    };
    directionsService.route(request, function(result, status) {
      if (status == 'OK') {
        directionsRenderer.setDirections(result);
      }
    });
  }




setInterval(async function () {
    let data = dataToSend();
    let responce_data = await fetch(url, {
        method: 'POST', 
        headers: {
            
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': true,
        },
        body: JSON.stringify(data),
    });
    data_f = await responce_data.json();
    console.log(data_f['connected']);

    if (data_f['connected'] == "false") {
        online_or_offline.textContent = "Offline";
        document.getElementById('live').style.background = '#F70606';
    }
    else if (data_f['connected'] == "true")
    {
        online_or_offline.textContent = "Online";
        document.getElementById('live').style.background = '#52DE20'
    }
    if (data_f["last_location"] != "Not -Yet startted") {
        last_location.textContent = data_f["last_location"];
    }
    if (data_f["next_location"] != "Not -Yet startted") {
        next_location.textContent = data_f["next_location"];
    }
    if(data_f["started"] == "true")
    {
        sheduled.style.background = '#449CED';
        sheduled_text.textContent = "Started";
    }
    time_live.textContent = data_f["times_ago"];
    console.log(data_f["times_ago"]);
    device_latitude = data_f["current_altitude"];
    device_longitude = data_f["current_longitude"];
    location_of_bus = new google.maps.LatLng(data_f["current_altitude"],data_f["current_longitude"]);
    let location = getLocation();
    location_of_me = new google.maps.LatLng(latitude,longitude);
    console.log("dta");
    console.log(data_f["current_longitude"]);
    console.log(data_f["current_longitude"]);
    marker_of_bus.setPosition(location_of_bus);
    
    let bus_loc = data_f["bus_stand"].split(",");
    
    
    if (times == 0){
        calcRoute(bus_loc[0],bus_loc[1],latitude,longitude);
    }
    times = times + 1;
    console.log(times);
    if(data_f["minutes_free"]!=0)
    {
        minutes_free.textContent = data_f["minutes_free"] + " minutes";
    }
    if(data_f["hours_free"]!=0)
    {
         hours_free.textContent = data_f["hours_free"] + " hours";
    }
    
   
    
    console.log(data_f["minutes_free"]);
    console.log(data_f["hours_free"]);
    
}, 10000);





let path = location.pathname;
let directories = path.split("/");
let tour_id = directories[(directories.length - 1)];
let online_or_offline = document.getElementById("live_text");
let last_location = document.getElementById("last_location");
let next_location = document.getElementById("next_location");
let bus_id = document.getElementById("bus_id").textContent;
let longitude = 0;
let latitude = 0;
let device_latitude = 0;
let device_longitude = 0;
const hours_free = document.getElementById("hours-free");
const minutes_free = document.getElementById("minutes-free");


const url = "http://127.0.0.1:80/api/js/";

const icon = "https://developers.google.com/maps/documentation/javascript/examples/full/images/info-i_maps.png";

function initMap(device_latitude, device_longitude, latitude, longitude) {

    let location = { lat: device_latitude, lng: device_longitude };
    let other_location = { lat: 6.044198 , lng: 80.241 };
    console.log(other_location);
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: location,
    });
    const marker = new google.maps.Marker({
        position: other_location,
        map: map,
    });

    let markert = new google.maps.Marker({

        position: location,
        icon: icon,
        type:"info",
        map: map,

    }
  

    );
    
}


let data;

function showPosition(position) {

    latitude = position.coords.latitude;
    longitude = position.coords.longitude;

    data = {
        'bus_id': bus_id,
        "latitude": latitude,
        "longtitude": longitude,
        "tour_id": tour_id,
    };
};

console.log(navigator.geolocation.getCurrentPosition(showPosition));

setInterval(async function () {
    console.log(data)
    let responce_data = await fetch(url, {
        method: 'POST',
        mode: 'no-cors', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify(data),
    })
    let data_f = await responce_data.json();
    console.log(data_f['connected'])
    initMap(data_f["current_altitude"], data_f["current_longitude"], latitude, longitude);
    if (data_f['connected'] == "false") {
        online_or_offline.textContent = "Offline";
        document.getElementById('live').style.background = '#F70606';
    }
    if (data_f["last_location"] != "Not -Yet startted") {
        last_location.textContent = data_f["last_location"];
    }
    if (data_f["next_location"] != "Not -Yet startted") {
        next_location.textContent = data_f["next_location"];
    }
    console.log(data_f["current_altitude"], data_f["current_longitude"]);
   
    
}, 10000);

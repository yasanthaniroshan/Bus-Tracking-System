



let path = location.pathname;
let directories = path.split("/");
let bus_id = directories[(directories.length - 1)];
let online_or_offline = document.getElementById("Online-text");
let longitude =0; 
let latitude=0;

const url = "http://127.0.0.1:8000/api/js/";

// function showPosition(position) {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(showPosition);
//     } else {
//         console.log("Geolocation is not supported by this browser.");
//     }

//     latitude = position.coords.latitude;
//     longitude = position.coords.longitude;
// }

// showPosition();



// async function getdata() {
//     let responce_data = await fetch(url, {
//         method: 'POST',
//         mode: 'no-cors', // or 'PUT'
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//     })
//     let data_f = await responce_data.json();
//     if (data_f['connected'] == "false") {
//         online_or_offline.textContent = "Offline"
//         document.getElementById('online-circle').style.background = 'red';
//     }
// }

// setInterval(async function () {
//     {
//         if (navigator.geolocation) {
//             navigator.geolocation.getCurrentPosition(showPosition);
//         } else {
//             console.log("Geolocation is not supported by this browser.");
//         }
//         function showPosition(position){
//         latitude = position.coords.latitude;
//         longitude = position.coords.longitude;
//         }
//     }

//     showPosition();

let data;

function showPosition(position) {
      
        latitude = position.coords.latitude;
        longitude= position.coords.longitude;
        
        data = {
            'bus_id': bus_id,
            "latitude": latitude,
            "longtitude": longitude,
        };
};

console.log(navigator.geolocation.getCurrentPosition(showPosition));

setInterval(async function(){
    console.log(data)
    let responce_data = await fetch(url, {
        method: 'POST',
        mode: 'no-cors', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    let data_f = await responce_data.json();
    console.log(data_f['connected'])
    if (data_f['connected'] == "false") {
        online_or_offline.textContent = "Offline";
        document.getElementById('online-circle').style.background = 'red';
    }
},20000);

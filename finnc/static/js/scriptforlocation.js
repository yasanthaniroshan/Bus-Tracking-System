let longitude = 0;
let latitude = 0;
function showPosition(position) {
    longitude = position.coords.longitude;
    latitude = position.coords.latitude;

    let startpoint = document.getElementById("starting-point");
    let option = document.createElement('option')
    option.textContent = "Your Location"
    let data = latitude.toString()+ "," +longitude.toString();
    option.value = data
    startpoint.add(option,0)
    
    console.log(data)
}
document.addEventListener('DOMContentLoaded', (event) => {
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
        document.getElementById('starting-point').disabled = false;
      } else {
        console.log('No GPS Data');
        document.getElementById('starting-point').disabled = false;
      }
})

document.getElementById('destination-point').addEventListener("change", startigpoint(this.value));

function startigpoint(val)
{
    document.getElementById('destination-point').disabled = false;
    console.log(val)
 
}
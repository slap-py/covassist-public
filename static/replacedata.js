function getLocation() {
    //Check if Geolocation is supported 
    if (navigator.geolocation) {
        //If supported, run the getCurrentPosition() method
        //If the getCurrentPosition() method is successful, it returns a coordinates object to the function specified in the parameter (showPosition)
        navigator.geolocation.getCurrentPosition(replaceData);
    } else {
        //If not, display a message to the user
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}
function replaceData(position){
    if(window.localStorage.getItem('userCounty') != null){
        county = window.localStorage.getItem('userCounty')
        state = window.localStorage.getItem('userState')
    }else{
        xmlHttpReq = new XMLHttpRequest()
        xmlHttpReq.open("GET",`/locations/county/${position.coords.latitude},${position.coords.longitude}`,false)
        xmlHttpReq.send(null)
        data = JSON.parse(xmlHttpReq.responseText)
        county = data[0]
        state = data[1]
        window.localStorage.setItem('userCounty',county)
        window.localStorage.setItem('userState',state)
    }
    

    xmlHttpReq = new XMLHttpRequest()
    xmlHttpReq.open("GET",`/cases/county/${county},${state}`,false)
    xmlHttpReq.send(null)
    data = JSON.parse(xmlHttpReq.responseText)

    //start replacing data
    // document.getElementById('today_cases').innerText = `Cases Today: ${data.newCases}`
    // document.getElementById('today_deaths').innerText = `Deaths Today: ${data.newDeaths}`

}
window.onload = getLocation();
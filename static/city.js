// Step 1: Get user coordinates
function getCoordintes() {
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };

    function success(pos) {
        var crd = pos.coords;
        var lat = crd.latitude.toString();
        var lng = crd.longitude.toString();
        var coordinates = [lat, lng];
        console.log(`Latitude: ${lat}, Longitude: ${lng}`);
        getCity(coordinates);
        return;

    }

    function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
    }

    navigator.geolocation.getCurrentPosition(success, error, options);
}

// Step 2: Get city name
function getCity(coordinates) {
    var xhr = new XMLHttpRequest();
    var lat = coordinates[0];
    var lng = coordinates[1];

    
    //caching
    if (window.localStorage.getItem('userCity') != null){
        city = window.localStorage.getItem('userCity')
        document.getElementById("city").innerHTML = "City: "+city;
    }else{
        //then get request
        xhr.open('GET', "https://us1.locationiq.com/v1/reverse.php?key=pk.e57a0f02b96029b11eaddbdc28d5638e&lat=" +
        lat + "&lon=" + lng + "&format=json", true);
        xhr.send();
        xhr.onreadystatechange = processRequest;
        xhr.addEventListener("readystatechange", processRequest, false);
    }

    
    

    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            var city = response.address.city;
            document.getElementById("city").innerHTML = "City: "+city;
            //make cache exist
            window.localStorage.setItem("userCity",city)
            return;
        }
    }
}

getCoordintes();
// Source: GeekForGeek
var map;
function initMap(){
    navigator.geolocation.getCurrentPosition(success, error);  
}
function success(position) {
    map = new google.maps.Map(document.getElementById("initmap"), {
        center: { lat: position.coords.latitude, lng: position.coords.longitude },
        zoom: 13
    });

    if(window.localStorage.getItem('nearbyVaxLocs') != null){
        data = JSON.parse(window.localStorage.getItem('nearbyVaxLocs'));
    }else{
        xmlHttpReq = new XMLHttpRequest();
        xmlHttpReq.open("GET", `/vaccineLocationDistance/${position.coords.latitude},${position.coords.longitude},15`, false);
        xmlHttpReq.send(null);
        data = JSON.parse(xmlHttpReq.responseText);
        console.log(data)
        window.localStorage.setItem('nearbyVaxLocs',JSON.stringify(data));
    }
    

    for (i = 0; i < data.length; i++) {
        marker = new google.maps.Marker({
            position: { lat: data[i].latitude, lng: data[i].longitude },
            map,
        });
        // console.log(marker)
        infowindow = new google.maps.InfoWindow({
            content: `<p>${data[i].loc_name}</p>
            <p>${data[i].loc_admin_street1}</p>
            <p>Vaccines Available:</p>
            <p>${data[i].med_name}</p>
            <a target="_blank" href='https://www.google.com/maps/dir/${position.coords.latitude},${position.coords.longitude}/${data[i].latitude},${data[i].longitude}'>Get Directions</a>
            <a href='/info/${data[i].index}'>More Info</a>`,
        })
        console.log(data[i])
        console.log(data[i].loc_name,data[i].index)
        google.maps.event.addListener(marker, 'click', (function (marker, infowindow) {
            return function () {
                infowindow.open(map, marker);
            };
        })(marker, infowindow));
        // google.maps.event.addListener(marker, 'click', function () {
        //     infowindow.open(map, marker);
        // });
        // infowindow.open(map, marker);
    }

    xmlHttpReq = new XMLHttpRequest();
    xmlHttpReq.open("GET", `/risk/${window.localStorage.getItem('userCounty')},${window.localStorage.getItem('userState')}`, false);
    xmlHttpReq.send(null);
    data = parseInt(xmlHttpReq.responseText);
    if (data === 1){
        document.getElementById("imgrisk").src = "https://cdn.discordapp.com/attachments/734876966863241276/932358369942077491/Untitled_design_3_1.png";
        document.getElementById("Risk_Level").innerHTML = "LOW";
        document.getElementById("Risk_Desc").innerHTML = "Just because the risk is low, that does not mean you should not take precautions! Please follow the COVID-19 Regulations by the CDC or your country's health department!.";
        console.log("test")
    } else if (data === 2){
        document.getElementById("imgrisk").src = "https://cdn.discordapp.com/attachments/734876966863241276/932358369942077491/Untitled_design_3_1.png";
        document.getElementById("Risk_Level").innerHTML = "LOW";
        document.getElementById("Risk_Desc").innerHTML = "Just because the risk is low, that does not mean you should not take precautions! Pease follow the COVID-19 Regulations by the CDC or your country's health department!" 
        console.log("test")
    } else if (data === 3) {
        document.getElementById("imgrisk").src = "https://cdn.discordapp.com/attachments/734876966863241276/932358298659864646/Untitled_design_2_1.png";
        document.getElementById("Risk_Level").innerHTML = "MEDIUM";
        document.getElementById("Risk_Desc").innerHTML = "Consider taking more steps to protect yourself and others from the virus. Please follow the COVID-19 Regulations by the CDC or your country's health department. Increase in cases is possible.";
        console.log("test")
    } else if (data === 4){
        document.getElementById("imgrisk").src = "https://cdn.discordapp.com/attachments/734876966863241276/932358433955520592/Untitled_design_4_1.png";
        document.getElementById("Risk_Level").innerHTML = "HIGH";
        document.getElementById("Risk_Desc").innerHTML = "Staying Indoors with family only is highly recommended, strictly follow precautions and regulations."
        console.log("test")
    } else if (data === 5) {
        document.getElementById("imgrisk").src = "https://cdn.discordapp.com/attachments/734876966863241276/932358433955520592/Untitled_design_4_1.png";
        document.getElementById("Risk_Level").innerHTML = "HIGH";
        document.getElementById("Risk_Desc").innerHTML = "Staying Indoors with family only is highly recommended, strictly follow precautions and regulations."
        console.log("test")
    }

    
}
function error(position) {
    if (error.code == error.PERMISSION_DENIED){
        window.location.href = "/";
        alert("To use this app, you must consent to sharing your location with this app. Please enable location sharing in your browser settings.");
    }
}
// window.onload = getLocation();
initMap();



//end map shit



function cases_location(){
    navigator.geolocation.getCurrentPosition(graphing);  
}
function graphing(position){
    xmlHttpReq = new XMLHttpRequest()
    if (window.localStorage.getItem('userCounty') != null){
        county = window.localStorage.getItem('userCounty')
        state = window.localStorage.getItem('userState')
    }else{
        xmlHttpReq.open("GET", `/locations/county/${position.coords.latitude},${position.coords.longitude}`, false)
        xmlHttpReq.send(null)
        d = JSON.parse(xmlHttpReq.responseText)
        county = d[0]
        state = d[1]
        //make cache exist
        window.localStorage.setItem('userCounty',county)
        window.localStorage.setItem('userState',state)
    }
    xmlHttpReq = new XMLHttpRequest()
    xmlHttpReq.open("GET", `/cases/ltm/${county},${state}`, false)
    xmlHttpReq.send(null)
    data = JSON.parse(xmlHttpReq.responseText)
    cases = data[0]
    deaths = data[1]
    dates = data[2]
    console.log("test")
    xmlHttpReq = new XMLHttpRequest()
    xmlHttpReq.open("GET", `/vaccinations/ltm/${county},${state}`, false)
    xmlHttpReq.send(null)
    data2 = JSON.parse(xmlHttpReq.responseText)
    initiated = data2[0]
    completed = data2[1]
    dates = data2[2]

    var xValues = dates;
    // var yValues = [12, 10, 9, 13, 9, 11, 10, 15, 14, 14, 15];
    // var xValues = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000];
    new Chart("myChart", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                tension: 0.4,
                data: data[0],
                borderColor: "blue",
                fill: false,
                label: "COVID Cases"
            }]
        },
        options: {
            legend: { display: false }
        }
    });
        new Chart("myChart2", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                tension: 0.4,
                data: data2[0],
                borderColor: "green",
                fill: false,
                // cubicInterpolationMode: 'linear',
                label: "Fully Vaccinated"
            },{
                tension: 0.4,
                data: data2[1],
                borderColor: "yellow",
                fill: false,
                // cubicInterpolationMode: 'linear',
                label: "Have At Least One Dose"
            }]
        },
        options: {
            legend: { display: true }
        }
    });
        new Chart("myChart3", {
            type: "line",
            data: {
                tension: 0.4,
                labels: xValues,
                datasets: [{
                    data: data[1],
                    borderColor: "red",
                    fill: false,
                    label: "Deaths"
                }]
            },
            options: {
                legend: { display: true }
            }
        });
}
cases_location();
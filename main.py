from flask import Flask, render_template
import flask
import json
import math
import requests
app = Flask('app')

data = json.loads(open('data/vaccines.json','r').read())
ptList = []

keys = json.loads(open('.secrets','r').read())
googleKey = keys['google']
covidKey = keys['covid']
cityKey = keys['city']


@app.route('/')
def index():
  return render_template("index.html")
@app.route('/docs')
def docs():
  return render_template("docs.html")
@app.route('/about')
def about():
  return render_template("about.html")
@app.route('/app')
def application():
  return render_template("app.html",googleKey=googleKey)
@app.route('/team')
def team():
  return render_template("team.html")
@app.route('/info/<idx>')
def info_page(idx):
  for location in data:
    if str(location['index']) == idx:
      #location found
      return render_template('info.html',name=location['loc_name'],address=location['loc_admin_street1'].title(),city=location['loc_admin_city'].title(),state=location['loc_admin_state'],vaxtypes=location['med_name'].split(' ')[0].replace(',',''),latitude=location['latitude'],longitude=location['longitude'],walkins=location['walkins_accepted'].replace('false','No').replace('true','Yes'),providInfo=location['provider_notes'],providWebsite=location['web_address'],prescreen=location['pre_screen'],sunhrs=location['sunday_hours'],monhrs=location['monday_hours'],tueshrs=location['tuesday_hours'],wedhrs=location['wednesday_hours'],thrushrs=location['thursday_hours'],frihrs=location['friday_hours'],sathrs=location['saturday_hours'])
@app.route('/vaccineLocation/<idx>')
def getvaxloc(idx):
  for location in data:
    if str(location['index']) == idx:
      return json.dumps(location)
  return flask.Response(response='This location does not currently exist',status=404)

def distancekey(e):
  return e['distance']
@app.route('/vaccineLocationDistance/<lat>,<lon>,<distance>')
def vaccineFromLoc(lat,lon,distance):
  lods = []
  lops = []
  for point in data:
    if len(str(point['longitude'])) < 3:
      pass
    else:
      point['latitude'] = float(point['latitude'])
      point['longitude'] = float(point['longitude'])
      lat = float(lat)
      lon = float(lon)
      distance = float(distance)
      latDistance = lat-point['latitude']
      latDistance = latDistance*110.574
      longDistance = lon-point['longitude']
      longDistance = longDistance*(111.320*math.cos(math.radians(lat)))
      
      if abs(latDistance)+abs(longDistance) < distance:
        if point['in_stock']:
          totalDistance = abs(latDistance)+abs(longDistance)
          point['distance'] = totalDistance
          #found point within distance
          #print(point['latitude'],point['longitude'])
          lods.append(totalDistance)
          lops.append(point)
  #sort
  lops.sort(key=distancekey)
  sorted_ = []
  for point in lops:
    if len(sorted_) < 30:
      sorted_.append(point)
    else:
      return json.dumps(sorted_)

@app.route('/cases/state/<state>')
def casesForState(state):
  data = requests.get('https://api.covidactnow.org/v2/states.json?apiKey={}'.format(covidKey)).json()
  for stateobj in data:
    if stateobj['state'].upper() == state.upper():
      toReturn = {
        'casesToday':stateobj['actuals']['newCases'],
        'deathsToday':stateobj['actuals']['newDeaths'],
        'hospitalData':{
          'capacity':stateobj['actuals']['hospitalBeds']['capacity'],
          'currentUsage':stateobj['actuals']['hospitalBeds']['currentUsageTotal'],
          'currentCovidUsage':stateobj['actuals']['hospitalBeds']['currentUsageCovid'],
          'percentFull':round(int(stateobj['actuals']['hospitalBeds']['currentUsageTotal'])/int(stateobj['actuals']['hospitalBeds']['capacity']),2)*100,
        },
        'icuData':{
          'capacity':stateobj['actuals']['icuBeds']['capacity'],
          'currentUsage':stateobj['actuals']['icuBeds']['currentUsageTotal'],
          'currentCovidUsage':stateobj['actuals']['icuBeds']['currentUsageCovid'],
          'percentFull':round(int(stateobj['actuals']['icuBeds']['currentUsageTotal'])/int(stateobj['actuals']['icuBeds']['capacity']),2)*100,
        },
        'vaccinationData':{
          'population':stateobj['population'],
          'vaccines':stateobj['actuals']['vaccinationsCompleted'],
          'percent':round(int(stateobj['actuals']['vaccinationsCompleted'])/stateobj['population'],2)*100,
        },

      }
      return toReturn

@app.route('/cases/county/<county>,<state>')
def casesForCounty(county,state):
  data = requests.get('https://api.covidactnow.org/v2/county/WA.timeseries.json?apiKey={}'.format(covidKey)).json()
  for stateobj in data:
    if stateobj['state'].upper() == state.upper():
      
      if county.lower() == stateobj['county'].lower():
        #previous data stays native from non-timeseries data
        return json.dumps(stateobj['actualsTimeseries'][-7])
        toRet = {
        'casesToday':stateobj['actuals']['newCases'],
        'deathsToday':stateobj['actuals']['newDeaths'],
        'hospitalData':{
          'capacity':stateobj['actuals']['hospitalBeds']['capacity'],
          'currentUsage':stateobj['actuals']['hospitalBeds']['currentUsageTotal'],
          'currentCovidUsage':stateobj['actuals']['hospitalBeds']['currentUsageCovid'],
          'percentFull':round(int(stateobj['actuals']['hospitalBeds']['currentUsageTotal'])/int(stateobj['actuals']['hospitalBeds']['capacity']),2)*100,
        },
        'icuData':{
          'capacity':stateobj['actuals']['icuBeds']['capacity'],
          'currentUsage':stateobj['actuals']['icuBeds']['currentUsageTotal'],
          'currentCovidUsage':stateobj['actuals']['icuBeds']['currentUsageCovid'],
          'percentFull':round(int(stateobj['actuals']['icuBeds']['currentUsageTotal'])/int(stateobj['actuals']['icuBeds']['capacity']),2)*100,
        },
        'vaccinationData':{
          'population':stateobj['population'],
          'vaccines':stateobj['actuals']['vaccinationsCompleted'],
          'percent':round(int(stateobj['actuals']['vaccinationsCompleted'])/stateobj['population'],2)*100,
        },
        'historicalData':{
          'cases':stateobj['actualsTimeseries'][-7]['cases'],
          'deaths':stateobj['actualsTimeseries'][-7]['deaths'],
          'icu':stateobj['actualsTimeseries'][-7]['icuBeds']['currentUsageTotal'],
          'hospital':stateobj['actualsTimeseries'][-7]['cases']['hospitalBeds']['currentUsageTotal'],
        }

        }


        return toRet
  return 'no'

@app.route('/locations/county/<lat>,<lon>')
def countyFromll(lat,lon):
  request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng={}, {}&key={}'.format(lat,lon,googleKey)).json()
  state = 'null'
  county = 'null'
  for component in request['results'][0]['address_components']:
    if component['types'][0] == 'administrative_area_level_2':
      county = component['long_name']
    elif component['types'][0] == 'administrative_area_level_1':
      state = component['short_name']
  return json.dumps([county,state])
@app.route('/cases/ltm/<countyn>,<state>')
def cases_last3months(countyn,state):
  data = requests.get('https://api.covidactnow.org/v2/county/WA.timeseries.json?apiKey={}'.format(covidKey)).json()
  deaths = []
  cases = []
  dates = []
  
  for county in data:
    countyname = county['county']
    if countyname.lower() == countyn.lower():

      timeseries = county['actualsTimeseries']
      for i in range(30,0,-1):
        i=-i
        timeserie = timeseries[i]
        deaths.append(timeserie['deaths'])
        cases.append(timeserie['cases'])
        dates.append(timeserie['date'])
      print(cases)
      return json.dumps([cases,deaths,dates])
  return json.dumps({'error':'county or state is wrong lmao'})

@app.route('/vaccinations/ltm/<countyn>,<state>')
def vaccinations_l3m(countyn,state):
  data = requests.get('https://api.covidactnow.org/v2/county/WA.timeseries.json?apiKey={}'.format(covidKey)).json()
  
  deaths = []
  cases = []
  dates = []
  
  for county in data:
    countyname = county['county']
    if countyname.lower() == countyn.lower():
      county_population = county['population']

      timeseries = county['actualsTimeseries']
      for i in range(-30,0):
        timeserie = timeseries[i]
        deaths.append(float(round(timeserie['vaccinationsInitiated']/county_population,3)*100))
        cases.append(float(round(timeserie['vaccinationsCompleted']/county_population,3)*100))
        dates.append(timeserie['date'])
      return json.dumps([cases,deaths,dates])
  return json.dumps({'error':'county or state is wrong lmao'})


@app.route('/risk/<countyn>,<state>')
def riskLevel(countyn,state):
  data = requests.get('https://api.covidactnow.org/v2/county/WA.json?apiKey={}'.format(covidKey)).json()
  for county in data:
    if county['county'].lower() == countyn.lower():
      #foudn the county
      riskLevel = county['riskLevels']['overall']
      return str(riskLevel)
  return 'no'

@app.route('/streetview/<address>')
def streetview(address):
  image = requests.get('https://maps.googleapis.com/maps/api/streetview?location={}&size=650x300&key={}'.format(address,googleKey))
  f = open('cache.img','wb')
  f.write(image.content)
  f.close()
  return flask.send_file('cache.img',mimetype='image/jpeg')


# if __name__ == "__main__":
app.run(debug=True)
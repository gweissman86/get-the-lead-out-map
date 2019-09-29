from csv import DictReader, DictWriter
from datetime import datetime
from googlemaps import Client
from os import environ
from requests import get
from time import sleep

infile = "ca_schools_lead_testing_data_september.csv"
timestamp = str(datetime.now()).split(".")[0].replace(" ", "_").replace("-","_").replace(":","_")
outfile = "ca_schools_lead_testing_data_september_geocoded_" + timestamp + ".csv"

def isFloat(string):
  try:
      float(string)
      return True
  except ValueError:
    return False

gmaps = Client(key=environ["GOOGLE_MAPS_API_KEY"])

with open(infile) as f:
  dictReader = DictReader(f)
  schools = list(dictReader)
  fieldnames = dictReader.fieldnames

with open(outfile, "w") as f:
  dictWriter = DictWriter(f, fieldnames=fieldnames)
  dictWriter.writeheader()

previous = 0
misses = 0
newly_geocoded = 0

def geocodeOSM(schoolAddress):
  print("\tstarting geocodeOSM")
  print("\tsleeping so we don't hammer the OSM API")
  sleep(10)
  params = {
    "addressdetails": 1,
    "format": "json",
    "q": schoolAddress,
    "state": "CA",
    "country": "US"
  }
  responses = get(url, params=params).json()
  if len(responses) > 0:
    print("\tgot at least one response from OSM")
    response = responses[0]
    address = response['address']
    city = address.get('city', None)
    county = address.get('county', None)
    latitude = response.get('lat', None)
    longitude = response.get('lon', None)
    state = response.get('state', None)
    if state == "California" and city and county and latitude and longitude:
      print("\tOSM response is good to go!")
      return {
        "city": city,
        "county": county,
        "latitude": latitude,
        "longitude": longitude
      }
    else:
      print("\tOSM response failed test")
  else:
    print("\tOSM geocoding returned 0 hits")

def geocodeGoogle(schoolAddress):
  print("\tstarting geocodeGoogle")
  geocode_results = gmaps.geocode(schoolAddress)
  if len(geocode_results) >= 1:
    print("\tgot at least one result from Google")
    geocode_result = geocode_results[0]
    print("gmaps geocode_result:", geocode_result)
    components = geocode_result['address_components']
    city = ([c['short_name'] for c in components if c['types'][0] == "locality"] or [None])[0]
    county = ([c['short_name'] for c in components if c['types'][0] == "administrative_area_level_2"] or [None])[0]
    state = ([c['short_name'] for c in components if c['types'][0] == "administrative_area_level_1"] or [None])[0]
    latitude = geocode_result['geometry']['location']['lat']
    longitude = geocode_result['geometry']['location']['lng']
    if state == "CA" and city and county and latitude and longitude:
      print("\tGoogle result passed test")
      return {
        "city": city,
        "county": county,
        "latitude": latitude,
        "longitude": longitude
      }
    else:
      print("\tGoogle result failed test")
  else:
    print("\tfailed to find any hits via Google")

for index, school in enumerate(schools):
  print("______________")
  if not isFloat(school['latitude']) or not isFloat(school['longitude']):
    url = "https://nominatim.openstreetmap.org/search"
    schoolAddress = school["schoolAddress"]
    print("schoolAddress:", schoolAddress)
    info = geocodeOSM(schoolAddress) or geocodeGoogle(schoolAddress)
    if info:
      print("info:", info)
      school['city'] = info['city']
      school['county'] = info['county']
      school['latitude'] = info['latitude']
      school['longitude'] = info['longitude']
      newly_geocoded += 1
    else:
      misses += 1
  else:
    previous += 1

  print("newly_geocoded:", newly_geocoded)
  print("previously geocoded:", previous)
  print("percentage missed:", float(misses) / (index+1))

  with open(outfile, "a") as f:
    DictWriter(f, fieldnames=fieldnames).writerow(school)
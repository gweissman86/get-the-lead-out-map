from csv import DictReader, DictWriter
from googlemaps import Client
from os import environ
from requests import get
from time import sleep

infile = "ca_schools_lead_testing_data_september.csv"
outfile = "ca_schools_lead_testing_data_september_geocoded.csv"

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

for index, school in enumerate(schools):
  print("\nindex:", index)
  if not isFloat(school['latitude']) or not isFloat(school['longitude']):
    url = "https://nominatim.openstreetmap.org/search"
    schoolAddress = school["schoolAddress"]
    params = {
      "addressdetails": 1,
      "format": "json",
      "q": schoolAddress,
      "state": "CA",
      "country": "US"
    }
    responses = get(url, params=params).json()
    if len(responses) > 0:
      response = responses[0]
      print("response:", response)
      address = response['address']
      school['city'] = address.get('city','')
      school['county'] = address.get('county', '')
      school['latitude'] = response['lat']
      school['longitude'] = response['lon']
      newly_geocoded += 1
    else:
      print("couldn't find via OSM: " + schoolAddress)
      geocode_results = gmaps.geocode(schoolAddress)
      if len(geocode_results) >= 1:
        geocode_result = geocode_results[0]
        print("geocode_result:", geocode_result)
        components = geocode_result['address_components']
        school['city'] = next(c['short_name'] for c in components if c['types'][0] == "locality")
        school['county'] = next(c['short_name'] for c in components if c['types'][0] == "administrative_area_level_2")
        school['latitude'] = geocode_result['geometry']['location']['lat']
        school['longitude'] = geocode_result['geometry']['location']['lng']
        print("\nschool:", school)
        newly_geocoded += 1
      else:
        print("couldn't find via Google:" + schoolAddress)
        misses += 1
    print("sleeping")
    sleep(10)
  else:
    previous += 1

  print("newly_geocoded:", newly_geocoded)
  print("previously geocoded:", previous)
  print("percentage missed:", float(misses) / (index+1))

  with open(outfile, "a") as f:
    DictWriter(f, fieldnames=fieldnames).writerow(school)
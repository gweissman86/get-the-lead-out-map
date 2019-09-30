import csv
import json


in_file = open('data/ca_schools_lead_testing_data_september_geocoded_2019_09_26_11_43_46.csv')

reader = csv.DictReader(in_file)

districts = {}

for line in reader:
    districtName = line['district']
    schoolName = line['school']
    
    if districtName not in districts: 
        districts[districtName] = {}

    districts[districtName][schoolName] = {'schoolAddress' : line['schoolAddress'], 'county' : line['county'], 'city' : line['city'], 'latitude' : line['latitude'], 'longitude' : line['longitude'], 'status' : line['status'], 'lead' : line['lead'], 'medianResult' : line['medianResult']}


# create JSON file and write 
with open("schools.json", "w") as write_file:
    json.dump(districts, write_file)

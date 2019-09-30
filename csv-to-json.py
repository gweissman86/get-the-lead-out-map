import csv
import json

infilepath = 'data/ca_schools_lead_testing_data_september_geocoded_2019_09_28_23_35_59_cleaned.csv'
in_file = open(infilepath)

reader = csv.DictReader(in_file)

districts = {}

for line in reader:
    districtName = line['district']
    schoolName = line['schoolName']

    if districtName not in districts:
        districts[districtName] = {}

    districts[districtName][schoolName] = {'schoolAddress' : line['schoolAddress'], 'county' : line['county'], 'city' : line['city'], 'latitude' : line['latitude'], 'longitude' : line['longitude'], 'status' : line['status'], 'lead' : line['lead'], 'medianResult' : line['medianResult']}


# create JSON file and write
with open("schools.json", "w") as write_file:
    json.dump(districts, write_file, indent=4)

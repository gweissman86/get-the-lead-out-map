import csv
import json

infilepath = 'data/ca_schools_lead_testing_data_september_geocoded_2019_09_28_23_35_59_cleaned.csv'
in_file = open(infilepath)

reader = csv.DictReader(in_file)

state = {
    "counties": {}
}

for line in reader:
    countyName = line['county']
    districtName = line['district']
    schoolName = line['schoolName']

    if countyName not in state['counties']:
        state['counties'][countyName] = { "districts": {} }

    if districtName not in state['counties'][countyName]['districts']:
        state['counties'][countyName]['districts'][districtName] = { "schools": {} }

    state['counties'][countyName]['districts'][districtName]['schools'][schoolName] = {'schoolAddress' : line['schoolAddress'], 'city' : line['city'], 'latitude' : line['latitude'], 'longitude' : line['longitude'], 'status' : line['status'], 'lead' : line['lead'], 'medianResult' : line['medianResult']}


# create JSON file and write
with open("data/schools.json", "w") as write_file:
    json.dump(state, write_file, indent=4)

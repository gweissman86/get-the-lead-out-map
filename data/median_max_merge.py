import pandas as pd

geocoded_data = pd.read_csv('ca_schools_lead_testing_data_september_geocoded_2019_09_28_23_35_59_cleaned.csv')
max_results = pd.read_csv('ca_schools_lead_testing_data_with_max_results.csv', usecols=['schoolName', 'schoolAddress', 'maxResult'])

median_and_max = pd.merge(geocoded_data, max_results, on=['schoolName', 'schoolAddress'], how='outer')

median_and_max.to_csv('ca_schools_median_max_lead_data.csv', index=False, compression=None)

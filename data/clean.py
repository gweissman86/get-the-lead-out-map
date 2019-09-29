from csv import DictWriter, DictReader

infile = "ca_schools_lead_testing_data_september_geocoded_2019_09_28_23_35_59.csv"
outfile = infile.replace(".csv","_cleaned.csv")

with open(infile) as f:
  reader = DictReader(f)
  fieldnames = reader.fieldnames

  outf = open(outfile, "w")
  writer = DictWriter(outf, fieldnames=fieldnames)
  writer.writeheader()

  for line in reader:
    if line["latitude"] != "NA":
      line["latitude"] = round(float(line["latitude"]), 6)
    if line["longitude"] != "NA":
      line["longitude"] = round(float(line["longitude"]), 6)
    writer.writerow(line)


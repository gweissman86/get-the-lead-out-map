from csv import DictWriter, DictReader

infile = "compressed.csv"
outfile = infile.replace(".csv","_cleaned.csv")

with open(infile) as f:
  reader = DictReader(f)
  fieldnames = reader.fieldnames

  outf = open(outfile, "w")
  writer = DictWriter(outf, fieldnames=fieldnames)
  writer.writeheader()

  for line in reader:
    if line["latitude"] != "NA" and line["latitude"] != "":
      line["latitude"] = round(float(line["latitude"]), 6)
    if line["longitude"] != "NA" and line["longitude"] != "":
      line["longitude"] = round(float(line["longitude"]), 6)
    writer.writerow(line)


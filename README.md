# get-the-lead-out-map
Online Interactive Map of Levels of Lead in Water in California Schools

# demo
https://geosurge.github.io/get-the-lead-out-map/

# setup
This command installs the protobuf compiler
```bash
npm run setup
```

# extra compression steps
1) Replace medianResult values of NA in compressed.csv with an empty string
2) Remove the unit column (fifth column) in the compressed.csv which isn't being used:
```cut -d, -f5 --complement compressed.csv > compressed-new.csv```

# contact
- Daniel Dufour (daniel@geosurge.io)
- Victoria Mak (victoria@geosurge.io)

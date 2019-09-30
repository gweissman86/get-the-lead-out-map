const { readFileSync, writeFileSync } = require("fs");
const { toObjects } = require('jquery-csv');
const text = readFileSync("ca_schools_lead_testing_data_geocoded.csv", "utf-8");
const rows = toObjects(text);
console.log("rows:", rows.length);
const geojson = {
  type: "FeatureCollection",
  features: rows.map(row => {
    return {
      type: "Feature",
      properties: row,
      geometry: {
        type: "Point",
        coordinates: [Number(row["longitude"]), Number(row["latitude"])]
      }
    };
  })
};

writeFileSync("schools.geojson", JSON.stringify(geojson, undefined, 2), "utf-8");

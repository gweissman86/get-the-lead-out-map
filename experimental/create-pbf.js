const { writeFileSync } = require('fs');
var protobuf = require("protobufjs");
var data = require('./data/schools.json');

protobuf.load('./data/school_data.proto', function(err, root) {
  if (err) throw err;


  /*
  var school = root.lookup("school_data.Districts.District.School");
  console.log("school:", school);

  var buffer = school.encode({
    schoolName: "USDHS"
  }).finish();
  console.log(buffer);
  */
  /*
  var district = root.lookup("school_data.Districts.District");
  console.log("district:", district);
  var buffer = district.encode({
    district: "San Diego Unified School District",
    schools: {
      "USDHS": {
        schoolName: "USDHS"
      }
    }
  }).finish();
  console.log(buffer);
  */

  var state = root.lookup("school_data.State");
  console.log(state);

  var buffer = state.encode(data).finish();
  console.log(buffer);

  writeFileSync('data/schools.pbf', buffer);

});
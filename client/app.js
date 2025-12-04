function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for(var i=0; i<uiBathrooms.length; i++) {
    if(uiBathrooms[i].checked) return parseInt(uiBathrooms[i].value);
  }
  return -1;
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for(var i=0; i<uiBHK.length; i++) {
    if(uiBHK[i].checked) return parseInt(uiBHK[i].value);
  }
  return -1;
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft").value;
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations").value;
  var estPrice = document.getElementById("uiEstimatedPrice");

  $.post('/predict_home_price', {
      total_sqft: parseFloat(sqft),
      bhk: bhk,
      bath: bathrooms,
      location: location
  }, function(data, status) {
      console.log(data.estimated_price);
      estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
  });
}

function onPageLoad() {
  console.log("Document loaded");
  $.get("/get_location_names", function(data, status) {
      console.log("got response for get_location_names request", data);
      if(data) {
          var locations = data.locations;
          var uiLocations = document.getElementById("uiLocations");
          $('#uiLocations').empty();
          $('#uiLocations').append('<option value="" disabled selected>Choose a Location</option>');
          for(var i=0; i<locations.length; i++) {
              var opt = new Option(locations[i], locations[i]);
              $('#uiLocations').append(opt);
          }
      }
  });
}

window.onload = onPageLoad;

// Set the base URL for API calls. 
// CRITICAL FIX: Since the Flask app serves both the HTML/JS AND the API, 
// they are on the same origin. We use the current window's protocol and hostname 
// without specifying a port (as Render uses standard HTTPS port 443).
const API_BASE_URL = window.location.protocol + '//' + window.location.host;

function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i=0; i<uiBathrooms.length; i++) {
        if(uiBathrooms[i].checked) return parseInt(uiBathrooms[i].value);
    }
    return -1; // Should ideally never happen if one is checked by default
}

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i=0; i<uiBHK.length; i++) {
        if(uiBHK[i].checked) return parseInt(uiBHK[i].value);
    }
    return -1; // Should ideally never happen if one is checked by default
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    
    // 1. Get input values
    var sqft = document.getElementById("uiSqft").value;
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations").value;
    var estPrice = document.getElementById("uiEstimatedPrice");

    // Input Validation
    if (!sqft || !bhk || !bathrooms || !location) {
        estPrice.innerHTML = "<h2>ERROR: Please fill all fields.</h2>";
        return;
    }

    // 2. Send POST request to the prediction API
    // Use the defined API_BASE_URL
    $.post(API_BASE_URL + '/predict_home_price', {
        total_sqft: parseFloat(sqft),
        bhk: bhk,
        bath: bathrooms,
        location: location
    }, function(data, status) {
        if (status === 'success' && data.estimated_price !== undefined) {
            console.log("Prediction successful:", data.estimated_price);
            // Format price to two decimal places
            const formattedPrice = data.estimated_price.toFixed(2);
            estPrice.innerHTML = "<h2>Estimated Price: " + formattedPrice.toString() + " Lakh</h2>";
        } else {
            console.error("Prediction failed or returned unexpected data:", data);
            estPrice.innerHTML = "<h2>Prediction Failed. Check Server Logs.</h2>";
        }
    }).fail(function(xhr, status, error) {
        console.error("API call error:", xhr.responseText);
        estPrice.innerHTML = "<h2>Error: Could not connect to server or API failed.</h2>";
    });
}

function onPageLoad() {
    console.log("Document loaded. Attempting to fetch locations.");
    
    // 1. Fetch locations from the server
    // Use the defined API_BASE_URL
    $.get(API_BASE_URL + "/get_location_names", function(data, status) {
        console.log("Got response for get_location_names request", data);
        
        if(status === 'success' && data && data.locations) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            
            // Add the default placeholder option
            $('#uiLocations').append('<option value="" disabled selected>Choose a Location</option>');
            
            // 2. Populate dropdown
            for(var i=0; i<locations.length; i++) {
                // Use location[i] for both the display text and the value
                var opt = new Option(locations[i].toUpperCase(), locations[i]); 
                $('#uiLocations').append(opt);
            }
        } else {
            console.error("Failed to load locations or server error:", data);
        }
    }).fail(function(xhr, status, error) {
        console.error("Error fetching locations:", xhr.responseText, status, error);
        // Display an error message to the user if locations can't be fetched
        var estPrice = document.getElementById("uiEstimatedPrice");
        estPrice.innerHTML = "<h2>Connection Error: Cannot load locations from server.</h2>";
    });
}

// Ensure the function runs when the entire window, including scripts, is loaded
window.onload = onPageLoad;

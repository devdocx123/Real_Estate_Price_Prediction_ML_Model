from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
import util
import os

app = Flask(__name__, static_folder=None)
# CORS is already enabled, which is good practice even though the Flask app is serving static files
# on the same domain.
CORS(app) 

# API routes
@app.route('/get_location_names')
def get_location_names():
    # Locations are returned in lowercase from util.py, which is correct for internal use.
    locations = util.get_location_names()
    print("Returning locations:", locations) # debug
    # Use jsonify for the response
    return jsonify({'locations': locations})

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    # Retrieve data from the POST request form
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
    except KeyError as e:
        return jsonify({'error': f'Missing form data: {e}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid data type: {e}'}), 400

    # Ensure location is converted to lowercase for model compatibility
    estimated_price = util.get_estimated_price(location.lower(), total_sqft, bath, bhk)
    return jsonify({'estimated_price': estimated_price})

# Serve frontend files
# This path setup assumes 'client' is one directory above the directory containing 'server.py'
CLIENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client'))

@app.route('/')
def index():
    # Serving index.html
    return send_from_directory(CLIENT_DIR, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    # Serving static files (app.js, style.css)
    # The path is modified from the browser request (e.g., /app.js) to the actual file (e.g., client/app.js)
    return send_from_directory(CLIENT_DIR, path)

# Main
if __name__ == "__main__":
    # Ensure the model artifacts are loaded before the server starts
    util.load_saved_artifacts()
    
    # CRITICAL RENDER FIX: Use the 'PORT' environment variable provided by Render 
    # for production, defaulting to a common port (like 5000) for local testing.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

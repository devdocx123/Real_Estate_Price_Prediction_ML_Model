from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # 1. Import CORS
import util
import os

# 1. You will need to install flask-cors: pip install flask-cors
# Use a non-static folder setup, as you are managing static serving manually
app = Flask(__name__, static_folder=None)
CORS(app) # 2. Enable CORS for all routes (essential for frontend/backend communication)

# API routes
@app.route('/get_location_names')
def get_location_names():
    # Locations are returned in lowercase from util.py, which is correct for internal use.
    locations = util.get_location_names()
    print("Returning locations:", locations) # debug
    # 3. Use jsonify for the response
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

    estimated_price = util.get_estimated_price(location.lower(), total_sqft, bath, bhk)
    return jsonify({'estimated_price': estimated_price})

# Serve frontend files
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
    util.load_saved_artifacts()
    # 4. Use a standard port like 8080 or 5000 for local development if not using a managed environment
    port = int(os.environ.get('PORT', 8080)) # Changed default to 8080 for common use
    app.run(host='0.0.0.0', port=port)

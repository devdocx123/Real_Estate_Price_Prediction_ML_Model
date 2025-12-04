from flask import Flask, request, jsonify, send_from_directory
import util
import os

app = Flask(__name__)

# ---------------- API Routes ----------------
@app.route('/get_location_names')
def get_location_names():
    locations = util.get_location_names()
    print("Returning locations:", locations)   # helpful debug
    response = jsonify({'locations': locations})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    estimated_price = util.get_estimated_price(location, total_sqft, bath, bhk)

    response = jsonify({'estimated_price': estimated_price})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ---------------- Serve Frontend ----------------
# Ensure correct absolute path to /client folder
CLIENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client'))

@app.route('/')
def index():
    return send_from_directory(CLIENT_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(CLIENT_DIR, path)

# ---------------- Main ----------------
if __name__ == '__main__':
    util.load_saved_artifacts()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

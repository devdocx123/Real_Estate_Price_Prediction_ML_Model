import pickle
import json
import numpy as np
import os

# Global variables to hold the model artifacts and data
__locations = None
__data_columns = None
__model = None

# CRITICAL: Define the base path relative to the current script (util.py)
# This handles the changing directory structure on the Render server.
_file_path = os.path.dirname(os.path.abspath(__file__))
# Assuming the artifacts (columns.json, model.pkl) are in the same directory as util.py
ARTIFACTS_PATH = _file_path 

def get_estimated_price(location, sqft, bath, bhk):
    # This function uses the loaded global artifacts
    try:
        # Find the index of the location in the data columns list
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # If location is not found, assume it's a new or rare location and use the first feature (which is usually total_sqft)
        loc_index = -1 

    # Create the input array for the model
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1 # Set the corresponding location dummy variable to 1

    # Return the prediction, rounded to 2 decimal places
    return round(__model.predict([x])[0], 2)

def load_saved_artifacts():
    print("Loading saved artifacts... start")
    global __data_columns
    global __locations
    global __model

    # 1. Load the data columns (including location list)
    columns_file_path = os.path.join(ARTIFACTS_PATH, "columns.json")
    try:
        with open(columns_file_path, 'r') as f:
            __data_columns = json.load(f)['data_columns']
            # The first 3 columns are general features (sqft, bath, bhk), the rest are locations
            __locations = __data_columns[3:]
        print("Successfully loaded data columns and location list.")
    except FileNotFoundError:
        print(f"ERROR: columns.json not found at {columns_file_path}")
        # Initialize with known basics if file is missing to prevent crash
        __data_columns = ['total_sqft', 'bath', 'bhk']
        __locations = []
        return # Stop if critical file is missing

    # 2. Load the trained model
    model_file_path = os.path.join(ARTIFACTS_PATH, "bangalore_home_prices_model.pkl")
    try:
        with open(model_file_path, 'rb') as f:
            __model = pickle.load(f)
        print("Successfully loaded trained model.")
    except FileNotFoundError:
        print(f"ERROR: Model file not found at {model_file_path}")
        return # Stop if critical file is missing

    print("Loading saved artifacts... done")

def get_location_names():
    # Return the loaded locations list
    return __locations

# Call the loading function once when util.py is first imported
# load_saved_artifacts() # This is now called in server.py's __main__ block, which is cleaner.

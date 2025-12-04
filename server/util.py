import json
import numpy as np
import pickle
import os
import warnings

warnings.filterwarnings("ignore")

__location = []
__data_columns = []
__model = None

def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1
        
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    
    if loc_index >= 0:
        x[loc_index] = 1
        
    estimated_price = __model.predict([x])[0]
    
    # Simple safeguard: ensure price is not negative
    return round(max(0, estimated_price), 2)

def get_location_names():
    # Returns the list of locations (in lowercase) for the frontend
    return __location

def load_saved_artifacts():
    global __data_columns, __location, __model
    
    # Ensures the base directory is correct relative to util.py location (server folder)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    columns_path = os.path.join(base_dir, "artifacts", "columns.json")
    model_path = os.path.join(base_dir, "artifacts", "bangalore_home_price_prediction_model.pickle")

    if os.path.exists(columns_path):
        with open(columns_path) as f:
            data = json.load(f)
            # data_columns includes sqft, bath, bhk, followed by location dummies
            __data_columns = data.get("data_columns", [])
            # Locations start from index 3 (after sqft, bath, bhk)
            __location = [loc.lower() for loc in __data_columns[3:]]
        print("Locations loaded successfully.")
    else:
        print(f"ERROR: columns.json missing at {columns_path}")

    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            __model = pickle.load(f)
        print("Model loaded successfully.")
    else:
        print(f"ERROR: model pickle missing at {model_path}")

if __name__ == "__main__":
    load_saved_artifacts()
    # Example test
    # print(get_estimated_price('rajaji nagar', 1000, 2, 2))

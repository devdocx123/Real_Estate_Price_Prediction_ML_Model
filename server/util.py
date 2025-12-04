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
    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __location

def load_saved_artifacts():
    global __data_columns, __location, __model
    base_dir = os.path.dirname(os.path.abspath(__file__))
    columns_path = os.path.join(base_dir, "artifacts", "columns.json")
    model_path = os.path.join(base_dir, "artifacts", "bangalore_home_price_prediction_model.pickle")

    if os.path.exists(columns_path):
        with open(columns_path) as f:
            data = json.load(f)
            __data_columns = data.get("data_columns", [])
            __location = [loc.lower() for loc in __data_columns[3:]]
        print("Locations:", __location)
    else:
        print("ERROR: columns.json missing!")

    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            __model = pickle.load(f)
        print("Model loaded")
    else:
        print("ERROR: model pickle missing!")

if __name__ == "__main__":
    load_saved_artifacts()

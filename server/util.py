import json
import numpy as np
import pickle
import warnings
import os

warnings.filterwarnings(action='ignore', category=UserWarning)

__location = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
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
    print("Loading saved artifacts... start")

    global __location
    global __data_columns
    global __model

    # 🔥 Correct absolute path for Render
    base_dir = os.path.dirname(os.path.abspath(__file__))

    columns_path = os.path.join(base_dir, "artifacts", "columns.json")
    model_path = os.path.join(base_dir, "artifacts", "bangalore_home_price_prediction_model.pickle")

    print("Loading columns from:", columns_path)
    print("Loading model from:", model_path)

    # Load columns.json
    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __location = __data_columns[3:]

    print("Locations loaded:", __location)

    # Load trained model
    with open(model_path, "rb") as f:
        __model = pickle.load(f)

    print("loading saved artifacts... done")


if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())

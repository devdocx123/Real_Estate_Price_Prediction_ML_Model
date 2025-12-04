import json
import numpy as np
import pickle
import warnings
import os

warnings.filterwarnings(action='ignore', category=UserWarning)

__location = []
__data_columns = []
__model = None


def get_estimated_price(location, sqft, bath, bhk):
    if not __data_columns or not __model:
        raise Exception("Artifacts not loaded!")

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
    global __location, __data_columns, __model

    base_dir = os.path.dirname(os.path.abspath(__file__))

    columns_path = os.path.join(base_dir, "artifacts", "columns.json")
    model_path = os.path.join(base_dir, "artifacts", "bangalore_home_price_prediction_model.pickle")

    print("Loading columns from:", columns_path)
    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __location = [x.title() for x in __data_columns[3:]]  # capitalize for dropdown

    print("Locations loaded:", __location)

    print("Loading model from:", model_path)
    with open(model_path, "rb") as f:
        __model = pickle.load(f)

    print("Artifacts loaded successfully.")

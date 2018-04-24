import os
import json


def read_full_data():
    path = os.path.join(os.path.dirname(__file__), "data.json")
    f = open(path, 'r')
    data_json = json.load(f)
    f.close()

    return data_json


def read_data_from_date():
    raise NotImplementedError

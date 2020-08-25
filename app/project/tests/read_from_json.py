import json


def extract_data_from_json_file(path_to_file, type_name):
    with open(path_to_file) as json_file:
        data = json.load(json_file)
    return data[type_name]

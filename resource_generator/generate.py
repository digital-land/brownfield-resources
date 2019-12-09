import json

def read_file(file):
    d = {}
    with open(file) as json_data:
        d = json.load(json_data)
        json_data.close()
    return d

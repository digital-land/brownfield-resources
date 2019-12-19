import json

from resource_generator.render import render_html
from resource_generator.utils import extract_file_name

def read_file(file):
    d = {}
    with open(file) as json_data:
        d = json.load(json_data)
        json_data.close()
    return d


def generate_from_file(file, static_folder):
    d = read_file(file)
    d['file_hash'] = extract_file_name(file)
    return render_html(d, static_folder)

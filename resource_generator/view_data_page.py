#!/usr/bin/env python3

import sys
import json
import datetime

import pandas as pd
from math import cos, radians

from resource_generator.renderer import Renderer
from resource_generator.data_analyser import DataAnalyser
from resource_generator.collection import CollectionIndex
from resource_generator.issue_mapper import extractFromIssuesFile
from resource_generator.filters import (
    readable_date,
    map_org_code_to_name,
    check_for_multiple,
    pluralise,
    map_media_type,
    is_valid_uri,
    extract_coord,
    issue_type_mapper,
    float_to_int)


def url_for_harmonised(resource_hash):
    return f'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/var/harmonised/{resource_hash}.csv'


def url_for_converted(resource_hash):
    return f'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/var/converted/{resource_hash}.csv'


def url_for_issues(resource_hash):
    return f'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/var/issue/{resource_hash}.csv'


def fetch_csv(url):
    print(f"...... collecting harmonised data from {url}")
    try:
        data = pd.read_csv(url, sep=",")
        # strip spaces introduced to values
        data_frame_trimmed = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # strip spaces introduced to column headers
        data_frame_trimmed = data_frame_trimmed.rename(columns=lambda x: x.strip())
        return data_frame_trimmed
    except Exception as e:
        print(f'FAILED: {e}')
        return {}


# roughly increase the size of the bounding box
# considers global to be perfect sphere
# see: https://stackoverflow.com/questions/4000886/gps-coordinates-1km-square-around-a-point
def increase_bounding_box(bbox, kms):
    earth_circumf_km = 40075
    # calculate the latitude difference
    lat_diff = kms * (360/earth_circumf_km)
    # calculate the longitude difference
    lat_in_rads = radians(bbox[2])
    line_of_long = cos(lat_in_rads) * earth_circumf_km
    long_diff = kms * (360/line_of_long)
    return (
        (bbox[0] - long_diff),
        (bbox[1] + long_diff),
        (bbox[2] - lat_diff),
        (bbox[3] + lat_diff)
    )


# where df is pandas data frame
def bounding_box(df):
    min_lng = df.GeoX.min()
    max_lng = df.GeoX.max()
    min_lat = df.GeoY.min()
    max_lat = df.GeoY.max()
    return (min_lng, max_lng, min_lat, max_lat)


# also need collection
ind = CollectionIndex()

# jinja setup
# dist_dir="../resource/docs/"
renderer = Renderer()
renderer.register_filter("readable_date", readable_date)
renderer.register_filter("map_org_code_to_name", map_org_code_to_name)
renderer.register_filter("check_for_multiple", check_for_multiple)
renderer.register_filter("pluralise", pluralise)
renderer.register_filter("map_media_type", map_media_type)
renderer.register_filter("is_valid_uri", is_valid_uri)
renderer.register_filter("extract_coord", extract_coord)
renderer.register_filter("issue_type_mapper", issue_type_mapper)
renderer.register_filter("float_to_int", float_to_int)


def formatIssuesData(issues):
    issues_by_row = {}
    for issue in issues:
        issues_by_row.setdefault(issue['row-number'], {"issue": []})
        issues_by_row[issue['row-number']]['issue'].append(issue)
    return issues_by_row


def print_failed_list(failed):
    print("Resources that failed to build are:")
    for r in failed:
        print(r)


# generates a page for all the resources in the index
def generate_all_playback_data_pages():
    created_successfully = []
    failed = []
    for resource_hash in ind.mappings['resource']:
        if generate_playback_data_page(resource_hash):
            created_successfully.append(resource_hash)
        else:
            failed.append(resource_hash)

    # print the results
    print("===================================")
    print(f"{len(created_successfully)} pages created, {len(failed)} pages failed")
    print("===================================")
    print_failed_list(failed)

    # generate the index page for /resource
    renderer.render_page("index.html", "index.html", resources=ind.mappings['resource'].keys(), ind=ind)


# generate a page for a given resource
def generate_playback_data_page(resource_hash):
    # fetch resource we are interested in
    data = fetch_csv(url_for_harmonised(resource_hash))
    json_data = json.loads(data.to_json(orient='records'))

    key_last_collected_from = ind.key_resource_last_collected_from(resource_hash)
    # analyse data
    analyser = DataAnalyser(json_data)

    # get the relevant issues for resource
    formatted_issues = extractFromIssuesFile(resource_hash)

    # render the page
    try:
        renderer.render_page(
            "view-data.html",
            f"{resource_hash}/index.html",
            data=json_data,
            summary=analyser.summary(),
            resource_hash=resource_hash,
            key_last_collected_from=key_last_collected_from,
            ind=ind,
            bbox=increase_bounding_box(bounding_box(data), 1),
            issues=formatted_issues,
            today=datetime.datetime.today().date().strftime('%Y-%m-%d'))
        print(f"SUCCESS: {resource_hash}")
        return True
    except Exception as e:
        print(f"Failed for: {resource_hash}")
        print(repr(e))
        return False


if __name__ == '__main__':
    # default resource hash
    resource_hash = "060e59f0475aa7d6fc8404bd325939d41442117775feed63fbd7ad1de5af8ac5"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            generate_all_playback_data_pages()
            sys.exit(0)
        else:
            resource_hash = sys.argv[1]
            print(f"Generate check data page for resource: {sys.argv[1]}")
    else:
        print(f"Generate check data page for default resource: {resource_hash}")
    generate_playback_data_page(resource_hash)

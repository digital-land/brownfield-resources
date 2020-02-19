#!/usr/bin/env python3

import sys
import json

from resource_generator.renderer import Renderer
from resource_generator.collection import CollectionIndex
from resource_generator.filters import readable_date, map_org_code_to_name

# need collection
ind = CollectionIndex()

# jinja setup
renderer = Renderer("https://digital-land-design.herokuapp.com/static")
#renderer.register_filter("readable_date", readable_date)
renderer.register_filter("map_org_code_to_name", map_org_code_to_name)


def sortResources(resource_list):
    _sorted = []
    for r in resource_list:
        last_collected = ind.date_resource_last_collected(r)
        _sorted.append({
            'resource': r,
            'last_collected': last_collected,
            'start_date': ind.date_resource_first_collected(r)
        })
    return sorted(_sorted, key=lambda x: x['start_date'])


# generate a page for a given resource
def generate_org_check_page(org_id):
    resources = ind.get_resources_for_org(org_id)
    _sorted_resources = sortResources(resources)
    other_resources = []
    if len(_sorted_resources) > 1:
        other_resources = _sorted_resources[:-1]

    # render the page
    try:
        renderer.render_page(
            "check-page-per-org.html",
            f"dataset/brownfield-land/organisation/{org_id}/check.html",
            organisation=org_id,
            ind=ind,
            latest_resource=_sorted_resources[-1],
            other_resources=other_resources)
        print(f"SUCCESS: {org_id}")
        return True
    except Exception as e:
        print(f"Failed for: {org_id}")
        print(repr(e))
        return False


if __name__ == '__main__':
    # default resource hash
    org_id = "local-authority-eng:NNO"
    if len(sys.argv) > 1:
        org_id = sys.argv[1]
        print(f"Generate check data page for resource: {sys.argv[1]}")
    else:
        print(f"Generate check data page for default resource: {org_id}")
    generate_org_check_page(org_id)

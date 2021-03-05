#!/usr/bin/env python3

import sys
import json

from resource_generator.renderer import Renderer
from resource_generator.filters import pluralise
from resource_generator.utils import read_csv

from digital_land_frontend.filters import (
    organisation_id_to_name_filter,
)

# jinja setup
renderer = Renderer(dist_dir="../dataset/docs")
renderer.register_filter("pluralise", pluralise)
renderer.register_filter("organisation_id_to_name", organisation_id_to_name_filter)


def index_by_org(resources):
    idx = {}
    for resource in resources:
        orgs = resource["organisations"].split(";")
        for org in orgs:
            idx.setdefault(org, {"resource": []})
            idx[org]["resource"].append(resource)
    return idx


def generate_all_check_pages():
    # get list of all resources
    all_resources = read_csv("data/resource.csv")
    index_resources = index_by_org(all_resources)
    for org in index_resources.keys():
        index_resources[org]["resource"].sort(key=lambda x: x["start-date"])
        generate_org_check_page(org, index_resources.get(org)["resource"])


# generate a page for a given resource
def generate_org_check_page(organisation, resources):

    # switch local-authority-eng:HGO to local-authority-eng/HGO
    curried_id = organisation.replace(":", "/")

    # render the page
    try:
        renderer.render_page(
            "check-page-per-org.html",
            f"brownfield-land/organisation/{curried_id}/check.html",
            organisation=organisation,
            latest_resource=resources[-1],
            other_resources=resources[:-1] if len(resources) > 1 else [],
        )
        print(f"SUCCESS: {organisation}")
        return True
    except Exception as e:
        print(f"Failed for: {organisation}")
        print(repr(e))
        return False


if __name__ == "__main__":
    # default resource hash
    org_id = "local-authority-eng:NNO"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            generate_all_check_pages()
            sys.exit(0)
        else:
            org_id = sys.argv[1]
            print(f"Generate check data page for resource: {sys.argv[1]}")
    else:
        print(f"Generate check data page for default resource: {org_id}")
    generate_org_check_page(org_id)

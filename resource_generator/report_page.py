#!/usr/bin/env python3

import jinja2

from collection import CollectionIndex, heat_map_data
from render import register_templates

from filters import colour_for_count

static_folder = "https://brownfield-sites-validator.herokuapp.com/static"

# register filters with jinja context
def register_filters(env):
    env.filters["countColour"] = colour_for_count

# set up mappings
ind = CollectionIndex()

# jinja setup
env = register_templates()
register_filters(env)

report_template = env.get_template("report.html")

weeks = heat_map_data('2019-11-01')

with open("tmp/report.html", "w") as f:
    f.write(report_template.render(static_folder=static_folder, mappings=ind.mappings, heat_map=weeks))

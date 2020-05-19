#!/usr/bin/env python3

import jinja2

from collection import CollectionIndex
from render import register_templates

static_folder = "https://digital-land-design.herokuapp.com/static"

# set up mappings
ind = CollectionIndex()
ind.print_resource_mapping()

# jinja setup
env = register_templates()

index_template = env.get_template("index.html")

resources = ind.mappings['resource'].keys()

with open("tmp/index.html", "w") as f:
    f.write(index_template.render(static_folder=static_folder, resources=resources, ind=ind))

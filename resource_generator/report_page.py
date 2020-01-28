#!/usr/bin/env python3

import jinja2
import datetime

from collection import CollectionIndex, heat_map_data, previous_day
from render import register_templates

from filters import colour_for_count, curie_org_url

static_folder = "https://digital-land-design.herokuapp.com/static"

# register filters with jinja context
def register_filters(env):
    env.filters["countColour"] = colour_for_count
    env.filters["curie_url"] = curie_org_url


# set up mappings
ind = CollectionIndex()

orgs_by_links = ind.orgs_by_no_links()

# jinja setup
env = register_templates()
register_filters(env)

global_params = {
    'url_base': 'https://digital-land.github.io/resource/'
}

report_template = env.get_template("report.html")

weeks = heat_map_data('2019-07-01')

def avg_new_resources_per_day(start_date):
    num_days = 0
    new_resource_count = 0
    today_str = datetime.datetime.today().date().strftime('%Y-%m-%d')
    day_str = today_str
    day_before_start = previous_day(start_date)
    while day_str != day_before_start:
        num_days = num_days + 1
        new_resource_count = new_resource_count + len(ind.new_resources(day_str))
        day_str = previous_day(day_str)
    return {
        'days': num_days,
        'new_resource_count': new_resource_count
    }

collection_start = "2019-11-01"
resource_count = avg_new_resources_per_day(collection_start)


with open("tmp/report.html", "w") as f:
    f.write(report_template.render(
        globals=global_params,
        static_folder=static_folder,
        ind=ind,
        mappings=ind.mappings,
        orgs_by_links=orgs_by_links,
        heat_map=weeks,
        today=datetime.datetime.today(),
        resource_count=resource_count)
    )

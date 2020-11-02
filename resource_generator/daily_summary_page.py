#!/usr/bin/env python3

import sys
import jinja2
import datetime

from resource_generator.collection import CollectionIndex, heat_map_data, previous_day
from resource_generator.render import register_templates
from resource_generator.renderer import Renderer

from resource_generator.filters import pluralise, curie_org_url

# set up mappings
ind = CollectionIndex()

orgs_by_links = ind.orgs_by_no_links()

# jinja setup
renderer = Renderer()
renderer.register_filter("pluralise", pluralise)
renderer.register_filter("curie_url", curie_org_url)

def generate_daily_summary_page(daystr):
    summary =  ind.generate_day_summary(daystr)
    new_resources = ind.new_resources(daystr)
    renderer.render_page(
        "daily-summary.html",
        f"tmp/log/{daystr}.html",
        daystr=daystr,
        ind=ind,
        summary=summary,
        new_resources=new_resources
    )

if __name__ == '__main__':
    #daystr = datetime.datetime.today().date().strftime('%Y-%m-%d')
    daystr = datetime.datetime.today().date().strftime('%Y-%m-%d')
    if len(sys.argv) > 1:
        daystr = sys.argv[1]
        print(f"Generate daily summary for {sys.argv[1]}")
    else:
        print(f"No date string provided. Generate daily summary for today: {daystr}")
    generate_daily_summary_page(daystr)

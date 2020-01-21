#!/usr/bin/env python3

import sys
import jinja2
import datetime

from collection import CollectionIndex, heat_map_data, previous_day
from render import register_templates

from filters import pluralise, curie_org_url

static_folder = "https://digital-land-design.herokuapp.com/static"

# register filters with jinja context
def register_filters(env):
    env.filters["pluralise"] = pluralise
    env.filters["curie_url"] = curie_org_url


# set up mappings
ind = CollectionIndex()

orgs_by_links = ind.orgs_by_no_links()

# jinja setup
env = register_templates()
register_filters(env)

summary_template = env.get_template("daily-summary.html")

def generate_daily_summary_page(daystr):
    summary =  ind.generate_day_summary(daystr)
    new_resources = ind.new_resources(daystr)
    with open(f"tmp/log/{daystr}.html", "w") as f:
        f.write(summary_template.render(
            static_folder=static_folder,
            daystr=daystr,
            ind=ind,
            summary=summary,
            new_resources=new_resources)
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

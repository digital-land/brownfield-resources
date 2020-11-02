#!/usr/bin/env python3

import os
import jinja2
import datetime

from resource_generator.utils import mkdir_p


class Renderer:

    def __init__(self, static_folder=None, dist_dir="tmp/resource/"):
        self.env = self.register_templates()
        self.static_folder = "https://digital-land.github.io"
        if static_folder is not None:
            self.static_folder = static_folder
        self.set_global({
            "staticPath": self.static_folder,
            "now": datetime.datetime.utcnow()
            })
        self.dist_dir = dist_dir

    def register_templates(self):
        multi_loader = jinja2.ChoiceLoader([
            jinja2.FileSystemLoader(searchpath="./resource_generator/templates"),
            jinja2.PrefixLoader({
                'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components'),
                'digital-land-frontend': jinja2.PackageLoader('digital_land_frontend')
            })
        ])
        return jinja2.Environment(loader=multi_loader)

    def register_filter(self, name, func):
        self.env.filters[name] = func

    def get_template(self, template_name):
        return self.env.get_template(template_name)

    def get_env(self):
        return self.env

    def set_global(self, globals):
        for k, v in globals.items():
            self.env.globals[k] = v

    def render_page(self, template, output_file, **kwargs):
        page_template = self.get_template(template)
        path = mkdir_p(output_file, self.dist_dir)
        print(f"Path to created file: {path}")
        with open(path, "w") as f:
            f.write(page_template.render(
                static_folder=self.static_folder,
                **kwargs)
            )

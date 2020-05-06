#!/usr/bin/env python3

import os
import jinja2

from resource_generator.utils import mkdir_p


class Renderer:

    def __init__(self, static_folder, dist_dir="tmp/resource/"):
        self.static_folder = static_folder
        self.env = self.register_templates()
        # TO DO: make this configurable
        self.dist_dir = dist_dir

    def register_templates(self):
        multi_loader = jinja2.ChoiceLoader([
            jinja2.FileSystemLoader(searchpath="./resource_generator/templates"),
            jinja2.PrefixLoader({
                'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components')
            })
        ])
        return jinja2.Environment(loader=multi_loader)

    def register_filter(self, name, func):
        self.env.filters[name] = func

    def get_template(self, template_name):
        return self.env.get_template(template_name)

    def render_page(self, template, output_file, **kwargs):
        page_template = self.get_template(template)
        path = mkdir_p(output_file, self.dist_dir)
        print(f"Path to created file: {path}")
        with open(path, "w") as f:
            f.write(page_template.render(
                static_folder=self.static_folder,
                **kwargs)
            )

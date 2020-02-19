#!/usr/bin/env python3

import os
import jinja2


dist_dir = "tmp/"


def mkdir_p(filename):
    path = os.path.join(dist_dir, filename)
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    return path


class Renderer:

    def __init__(self, static_folder):
        self.static_folder = static_folder
        self.env = self.register_templates()

    def register_templates(self):
        multi_loader = jinja2.ChoiceLoader([
            jinja2.FileSystemLoader(searchpath="./resource_generator/templates"),
            jinja2.PrefixLoader({
                'govuk-jinja-components': jinja2.PackageLoader('govuk-jinja-components')
            })
        ])
        return jinja2.Environment(loader=multi_loader)

    def register_filter(self, name, func):
        self.env.filters[name] = func

    def get_template(self, template_name):
        return self.env.get_template(template_name)

    def render_page(self, template, output_file, **kwargs):
        page_template = self.get_template(template)
        path = mkdir_p(output_file)
        print(f"Path to created file: {path}")
        with open(path, "w") as f:
            f.write(page_template.render(
                static_folder=self.static_folder,
                **kwargs)
            )

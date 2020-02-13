#!/usr/bin/env python3

import jinja2


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

    def render_page(self, template, output, **kwargs):
        page_template = self.get_template(template)
        with open(output, "w") as f:
            f.write(page_template.render(
                static_folder=self.static_folder,
                **kwargs)
            )

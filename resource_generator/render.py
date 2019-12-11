import jinja2

from resource_generator.filters import pluralise


# set up paths to where the templates are
def register_templates():
    multi_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(searchpath="./resource_generator/templates"),
        jinja2.PrefixLoader({
            'govuk-jinja-components': jinja2.PackageLoader('govuk-jinja-components')
        })
    ])
    return jinja2.Environment(loader=multi_loader)


# register filters with jinja context
def register_filters(env):
    env.filters["pluralise"] = pluralise


# jinja setup
env = register_templates()
register_filters(env)


def render_html(data, static_folder):
    test_template = env.get_template("test.html")
    html = test_template.render(report=data, static_folder=static_folder)
    return html
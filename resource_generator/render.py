import jinja2

from resource_generator.filters import pluralise

loader = jinja2.FileSystemLoader(searchpath="./resource_generator/templates")
env = jinja2.Environment(loader=loader)


def register_filters(env):
    env.filters["pluralise"] = pluralise


register_filters(env)


def render_html(data):
    test_template = env.get_template("test.html")
    return test_template.render(report=data)
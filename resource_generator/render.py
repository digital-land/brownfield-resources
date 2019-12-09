import jinja2

loader = jinja2.FileSystemLoader(searchpath="./resource_generator/templates")
env = jinja2.Environment(loader=loader)

test_template = env.get_template("test.html")

def render_html(data):
    return test_template.render(report=data)
import jinja2
import markdown

from resource_generator.filters import pluralise, curie_org_url


# set up paths to where the templates are
def register_templates():
    multi_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(searchpath="./resource_generator/templates"),
        jinja2.PrefixLoader({
            'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components')
        })
    ])
    return jinja2.Environment(loader=multi_loader)


def markdown_filter(env):
    md = markdown.Markdown()
    env.filters["markdown"] = lambda text: jinja2.Markup(md.convert(text))


# register filters with jinja context
def register_filters(env):
    env.filters["pluralise"] = pluralise
    env.filters["curie_url"] = curie_org_url
    markdown_filter(env)


# jinja setup
env = register_templates()
register_filters(env)


def render_html(data, resource_metadata, static_folder, collection_index):
    resource_template = env.get_template("result.html")
    html = resource_template.render(
            report=data,
            static_folder=static_folder,
            resource_metadata=resource_metadata,
            ind=collection_index
        )
    return html
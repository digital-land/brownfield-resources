import sys
import click

from resource_generator.generate import generate_from_file

@click.command()
@click.option("--file", help="The path to the result json", required=True)
@click.option(
    "--static-folder",
    default="/static",
    help="Set the path to the folder of static assets"
)
@click.option(
    "--output", help="Path of the output file", required=False
)
def generate(file, static_folder, output):
    try:
        html = generate_from_file(file, static_folder)
        if output:
            with open(output, "w") as f:
                print(html, file=f)
        else:
            print(html)
        sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    generate()

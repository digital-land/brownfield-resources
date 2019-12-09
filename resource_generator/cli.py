import sys
import click

from resource_generator.generate import read_file

@click.command()
@click.option("--file", help="The path to the result json", required=True)
def generate(file):
    try:
        print(read_file(file))
        sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    generate()

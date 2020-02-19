import os
import sys
import glob
import click

from resource_generator.generate import generate_from_file
from resource_generator.collection import CollectionIndex
from resource_generator.utils import mkdir_p

collection_ind = CollectionIndex()


@click.command()
@click.option("--file", help="The path to the result json")
@click.option("--input-dir", help="The path to directory containing json result files")
@click.option(
    "--static-folder",
    default="https://brownfield-sites-validator.herokuapp.com/static",
    help="Set the path to the folder of static assets"
)
@click.option(
    "--output-file", help="Path of the output file", required=False
)
@click.option(
    "--output-dir", help="Directory to output HTML files", required=False
)
def generate(file, input_dir, static_folder, output_file, output_dir):
    # default output dir if not set
    output_dir = make_valid_dir(output_dir) if output_dir else "tmp/resource/"

    if file:
        # check if output file is known
        if not output_file:
            output_file = get_output_file(file, output_dir)
        if generate_single_resource(file, static_folder, output_file):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        if input_dir and os.path.isdir(input_dir):
            print(f"Looking for data files in {input_dir}")
            data_files = glob.glob(f"{input_dir}/*.json")
        else:
            print("No file give. Attempting to batch generate from DIRECTORY.")
            current_dir = os.getcwd()
            print(f"Looking for data files in {current_dir}")
            data_files = glob.glob(f"{current_dir}/data/*.json")

        if len(data_files) > 0:
            for filename in data_files:
                print(f"Generating resource page for...... {filename}")
                output_file = get_output_file(filename, output_dir)
                if generate_single_resource(filename, static_folder, output_file):
                    print(f"Successfully generated {output_file}")
                else:
                    print("Unable to generate resource page")
        else:
            print("No data files found.")
            sys.exit(1)


def make_valid_dir(d):
    return os.path.join(d, "")


def get_output_file(filename, output_dir):
    base = os.path.basename(filename)
    return os.path.join(output_dir, os.path.splitext(base)[0], "validation-result.html")


def generate_single_resource(filename, static_folder, output):

    try:
        html = generate_from_file(filename, static_folder, collection_ind)
        # create any directories that don't exist
        mkdir_p(output)
        with open(output, "w") as f:
            print(html, file=f)
        return True
        # sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        # sys.exit(1)
        return False


if __name__ == '__main__':
    generate()

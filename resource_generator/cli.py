import os
import sys
import glob
import click

from resource_generator.generate import generate_from_file

@click.command()
@click.option("--file", help="The path to the result json")
@click.option(
    "--static-folder",
    default="/static",
    help="Set the path to the folder of static assets"
)
@click.option(
    "--output", help="Path of the output file", required=False
)
def generate(file, static_folder, output):

    if file:
        if generate_single_resource(file, static_folder, output):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("No file give. Attempting to batch generate from DIRECTORY.")
        current_dir = os.getcwd()
        print(f"Looking for data files in {current_dir}")
        data_files = glob.glob(f"{current_dir}/data/*.json")
        if len(data_files) > 0:
            for filename in data_files:
                print(f"Generating resource page for...... {filename}")
                if generate_single_resource(filename, static_folder, None):
                    print("Successfully generated")
                else:
                    print("Unable to generate resource page")
        else:
            print("No data files found.")
            sys.exit(1)


def generate_single_resource(filename, static_folder, output):
    tmp_dir = "tmp/"

    try:
        html = generate_from_file(filename, static_folder)
        if output:
            with open(output, "w") as f:
                print(html, file=f)
        else:
            base = os.path.basename(filename)
            output_file = tmp_dir + os.path.splitext(base)[0] + ".html"
            with open(output_file, "w") as f:
                print(html, file=f)
        return True
        #sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        #sys.exit(1)
        return False


if __name__ == '__main__':
    generate()

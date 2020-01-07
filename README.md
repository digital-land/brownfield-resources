## Brownfield resource generator

Takes report json from the brownfield validator as input and generates an HTML page to present the results.

### To use

Install dependencies

    pipenv install

Generate HTML with

    brownfield-resource-gen --file path/to/result.json

Batch generate HTML resource pages with

    brownfield-resource-gen

Batch generating requires there to be .json result files in the `/data` directory or a directory of your choosing. You can set the directory with

    brownfield-resource-gen --input-dir /path/to/input/dir

It will output the HTML files to `/tmp` or a directory you define with

    brownfield-resource-gen --input-dir /path/to/input/dir --output-dir /path/to/output/dir

To generate all the brownfield resource pages found at [digital-land/resource](https://digital-land.github.io/resource) you will first need to check out the [brownfield-land-collection](https://github.com/digital-land/brownfield-land-collection) repo. Then the `--input-dir` should point to the `validation` dir in this repo.


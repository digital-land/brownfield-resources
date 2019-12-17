## Brownfield resource generator

Takes report json from the brownfield validator as input and generates an HTML page to present the results.

### To use

Install dependencies

    pipenv install

Generate HTML with

    brownfield-resource-gen --file path/to/result.json

Batch generate HTML resource pages with

    brownfield-resource-gen

Batch generating requires there to be .json result files in the `/data` directory. It will output the HTML files to `/tmp`.


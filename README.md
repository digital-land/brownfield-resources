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

### Additional uses

Scripts in this repo can be used to generate other pages.

To generate an `index.html` page for the resource pages, run

    python resource_generator/index.py

To generate a `report.html` page (contains stats on what the collector does), run

    python resource_generator/report_page.py

To generate daily summary log pages, run

    python resource_generator/daily_summary_page.py <day_str>

where `day_str` is the day you wish the log page to cover, e.g. `2020-01-21`. This creates the pages in `tmp/log`.

To generate view data pages, run

    python resource_generator/check_data_page.py <resource_hash>

where `resource_hash` is the id of a collected resource. E.g. `77da1087f91eafee42797dbaa9bebef573d2eb759b39d9db130c99d34cbe4ec4`

### Issues

`daily_summary_page.py` for **2019-12-24**, need to investigate

### Steps to run daily

- checkout latest from [the collector](https://github.com/digital-land/brownfield-land-collection)
- generate resource pages with `brownfield-resource-gen`
- generate index pages with `python resource_generator/index.py`
- generate latest report page with `python resource_generator/report.py`
- generate any outstanding daily log pages e.g. `python resource_generator/daily_summary_page.py 2020-01-2`
- copy generated files into **/docs** directory of [resource repo](https://github.com/digital-land/resource)
- commit **resource repo**

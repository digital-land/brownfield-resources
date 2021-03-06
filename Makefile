init:
	pip install -r requirements.txt

view-data-pages:
	python resource_generator/view_data_page.py --all

check-data-pages:
	python resource_generator/check_per_org.py --all

render:
	python3 resource_generator/view_data_page.py --all && \
	python3 resource_generator/report_page.py && \
	python3 resource_generator/daily_summary_page.py && \
	python3 resource_generator/cli.py --input-dir ../brownfield-land-collection/validation

collect::
	mkdir -p data
	curl -qsL 'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/main/collection/resource.csv' > data/resource.csv
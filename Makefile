init:
	pip install -r requirements.txt

view-data-pages:
	python resource_generator/check_data_page.py --all

check-data-pages:
	python resource_generator/check_per_org.py --all
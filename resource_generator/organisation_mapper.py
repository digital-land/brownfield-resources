import os
import csv

# needs to be where you have the organisation collection checked out
data_dir = "../organisation-collection/collection/"
organisation_csv = 'organisation.csv'
cvs_file_path = os.path.join(data_dir, organisation_csv)


class OrganisationMapping:

    def __init__(self):
        self.organisation_mapping = {}
        with open(cvs_file_path, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                key = row['organisation']
                self.organisation_mapping[key] = row['name']

    def get_organisation_name(self, organisation_id):
        return self.organisation_mapping.get(organisation_id)

    def order_by_name(self):
        sorted_mapping = sorted(self.organisation_mapping.items(), key=lambda kv: kv[1])
        return sorted_mapping

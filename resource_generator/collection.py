import json
import urllib.request

from collections import defaultdict

class CollectionIndex:
    
    def __init__(self):
        self.index_url = "https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/collection/index.json"
        response = urllib.request.urlopen(self.index_url)
        self.index = json.loads(response.read())
        self.mappings = {}
        self.create_mapping()

    def get_key(self, key_hash):
        return self.index['key'][key_hash]

    def get_resource(self, resource_hash):
        return self.index['resource'][resource_hash]

    def create_mapping(self):
        self.mapping = {}
        self.create_key_to_resources_mapping()
        self.create_resouce_to_keys_mapping()

    def create_resouce_to_keys_mapping(self):
        self.mappings['resource'] = defaultdict(set)
        for k in self.index['key']:
            # loop through each log entry
            for entry in self.index['key'][k]['log']:
                # look for resource
                if 'resource' in self.index['key'][k]['log'][entry]:
                    resource_hash = self.index['key'][k]['log'][entry]['resource']
                    self.mappings['resource'][resource_hash].add(k)

    def create_key_to_resources_mapping(self):
        self.mappings['key'] = {}
        for k in self.index['key']:
            self.mappings['key'][k] = self.get_resources_for_key(k)

    def get_keys_for_resource(self, resource_hash):
        return list(self.mappings['resource'][resource_hash])

    def get_resources_for_key(self, key_hash):
        log = self.get_key_log(key_hash)
        return list(set([log[l]['resource'] for l in log if 'resource' in log[l]]))

    def extract_metadata(self, resource_hash):
        keys = self.get_keys_for_resource(resource_hash)
        collection_entry = self.get_key(keys[0])
        return {
            'hash': resource_hash,
            'organisation': list(collection_entry['organisation'].keys())[0],
            'row_count': self.get_resource(resource_hash)['row-count']
        }

    def get_key_log(self, key_hash):
        return self.get_key(key_hash)['log']

    def date_key_first_collected(self, key_hash):
        log = self.get_key_log(key_hash)
        return sorted(log)[0]

    def date_key_last_collected(self, key_hash):
        log = self.get_key_log(key_hash)
        return sorted(log, reverse=True)[0]

    def print_resource_mapping(self):
        for r in self.mappings['resource']:
            if len(self.get_keys_for_resource(r)) > 1:
                #print(f"{r} maps to {len(self.get_keys_for_resource(r))} keys")
                print(f"Resource: {r}")
                for k in self.get_keys_for_resource(r):
                    print(f"-- key: {self.index['key'][k]['url']} first {self.date_key_first_collected(k)} last {self.date_key_last_collected(k)}")

    def print_key_mapping(self):
        for k in self.index['key']:
            print(f"Key:{k} has resources [{self.mappings['key'][k]}]")

    def print_organisations(self):
        for k in self.index['key']:
            print(f"Key: {k} associated with orgs [{self.index['key'][k]['organisation'].keys()}]")
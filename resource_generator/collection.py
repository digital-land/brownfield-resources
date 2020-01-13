import json
import datetime
import urllib.request

from collections import defaultdict, Counter


def previous_day(daystr):
    d = datetime.datetime.strptime(daystr, '%Y-%m-%d')
    pd = d - datetime.timedelta(days=1)
    return pd.strftime('%Y-%m-%d')


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
        self.map_keys_to_organisations()


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
        resources = {}
        for item in log:
            if 'resource' in log[item].keys():
                resources.setdefault(log[item]['resource'], {"logged_on": []})
                resources[log[item]['resource']]["logged_on"].append(item)
        return resources
        #return list(set([log[l]['resource'] for l in log if 'resource' in log[l]]))

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

    def get_key_url(self, key_hash):
        return self.get_key(key_hash)['url']

    def date_key_first_collected(self, key_hash):
        log = self.get_key_log(key_hash)
        return sorted(log)[0]

    def date_key_last_collected(self, key_hash):
        log = self.get_key_log(key_hash)
        return sorted(log, reverse=True)[0]


    def map_keys_to_organisations(self):
        self.mapping['organisation'] = {}
        idx = self.index
        for k in self.index['key']:
            for org in self.index['key'][k]["organisation"]:
                self.mapping["organisation"].setdefault(org, {"key": []})
                self.mapping["organisation"][org]["key"].append(k)


    def print_resource_mapping(self):
        for r in self.mappings['resource']:
            if len(self.get_keys_for_resource(r)) > 1:
                #print(f"{r} maps to {len(self.get_keys_for_resource(r))} keys")
                print(f"Resource: {r}")
                for k in self.get_keys_for_resource(r):
                    print(f"-- key: {self.index['key'][k]['url']} first {self.date_key_first_collected(k)} last {self.date_key_last_collected(k)}")

    def print_key_mapping(self):
        for k in self.index['key']:
            if len(self.mappings['key'][k]) > 1:
                print(f"Key:{self.index['key'][k]['url']}")
                for res in self.mappings['key'][k].keys():
                    log_dates = self.mappings['key'][k][res]['logged_on']
                    log_dates.sort()
                    print(f"---- {res} first seen {log_dates[:1]} and last seen {log_dates[-1:]}")
                    #print(f"---- {res} logged_on {self.mappings['key'][k][res]['logged_on']}")
                    #print(f"Key:{self.index['key'][k]['url']} has resources [{self.mappings['key'][k]}]")
                    #print(f"Key:{k} has resources [{self.mappings['key'][k]}]")

    def print_organisations(self):
        for k in self.index['key']:
            print(f"Key: {k} associated with orgs [{self.index['key'][k]['organisation'].keys()}]")


    def if_fetched_on_date(self, log, datestr):
        for d in log:
            if d == datestr:
                return True

    def print_day_summary(self, daystr):
        fetched_on_day = 0
        status_codes = []
        for k in self.index['key']:
            if self.if_fetched_on_date(self.index['key'][k]['log'], daystr):
                fetched_on_day = fetched_on_day + 1
                if 'status' in self.index['key'][k]['log'][daystr].keys():
                    status_codes.append(self.index['key'][k]['log'][daystr]['status'])
                else:
                    status_codes.append(self.index['key'][k]['log'][daystr]['exception'])
                    #print(f"No status for {k}:")
                    #print(f"----- {self.index['key'][k]['log'][daystr]}")
                #print(f"{self.index['key'][k]['url']} was fetched today")
        print(f"Attempted to fetch from {fetched_on_day} URLs")
        print(Counter(status_codes))

    def print_today_summary(self):
        today = datetime.datetime.today().date().strftime('%Y-%m-%d')
        self.print_day_summary(today)
import json
import datetime
import urllib.request

from collections import defaultdict, Counter


def previous_day(daystr):
    d = datetime.datetime.strptime(daystr, '%Y-%m-%d')
    pd = d - datetime.timedelta(days=1)
    return pd.strftime('%Y-%m-%d')

def days_between(day1, day2):
    d1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(day2, '%Y-%m-%d')
    # abs makes sure an absolute number is returned e.g. a +ve number
    return abs((d1-d2).days)

def date_x_days_before(daystr, x):
    d = datetime.datetime.strptime(daystr, '%Y-%m-%d')
    pd = d - datetime.timedelta(days=x)
    return pd.strftime('%Y-%m-%d')

def days_since_first_monday_of_month(month_str):
    day_number = datetime.datetime.today().weekday()
    today = datetime.datetime.today().date().strftime('%Y-%m-%d')
    between = days_between(month_str, today)
    remainder = (between - day_number) % 7
    # +1 is needed to include today
    return (between - remainder) + 1

def create_week_blocks(num_days):
    weeks = {}
    day_num = 0
    week_num = 1
    today_str = datetime.datetime.today().date().strftime('%Y-%m-%d')
    for d in range(num_days):
        if day_num == 0:
            weeks.setdefault(str(week_num), [])
        days_ago = num_days - (d+1)
        weeks[str(week_num)].append(date_x_days_before(today_str, days_ago))
        if day_num == 6:
            day_num = 0
            week_num = week_num + 1
        else:
            day_num = day_num + 1
    return weeks

def heat_map_data(startdate):
    days_since_start = days_since_first_monday_of_month(startdate)
    weeks = create_week_blocks(days_since_start)

    ind = CollectionIndex()

    for w in weeks:
        weeks[w] = [(d, len(ind.new_resources(d))) for d in weeks[w]]
    return weeks


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
        # works out which keys a resource appears in
        resources = defaultdict(set)
        for k in self.index['key']:
            # loop through each log entry
            for entry in self.index['key'][k]['log']:
                # look for resource
                if 'resource' in self.index['key'][k]['log'][entry]:
                    resource_hash = self.index['key'][k]['log'][entry]['resource']
                    resources[resource_hash].add(k)


        # index keys for a resource with the dates it was logged
        self.mappings['resource'] = {}
        for resource_hash in resources:
            self.mappings['resource'][resource_hash] = {}
            for key in resources[resource_hash]:
                log = self.index['key'][key]['log']
                dates = [d for d in log if 'resource' in log[d] and log[d]['resource'] == resource_hash]
                self.mappings['resource'][resource_hash].setdefault(key, {"logged_on": []})
                self.mappings['resource'][resource_hash][key]['logged_on'] = dates


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

    
    # returns dict
    #   {
    #       'type': {'resource': [res_hash, res_hash, res_hash]}
    #   }
    def resource_types(self):
        types = {}
        for resource_hash in self.index['resource']:
            resource = self.get_resource(resource_hash)
            types.setdefault(resource['media-type'], {"resource": []})
            types[resource['media-type']]["resource"].append(resource_hash)
        return types


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

    def concat_all_dates_resource_logged(self, resource_hash):
        resource = self.mappings['resource'][resource_hash]
        dates = []
        for k in resource:
            dates = dates + resource[k]['logged_on']
        return list(set(dates))

    def date_resource_first_collected(self, resource_hash):
        dates = self.concat_all_dates_resource_logged(resource_hash)
        return sorted(dates)[0]

    def date_resource_first_collected_from_key(self, resource_hash, key_hash):
        dates = self.mappings['resource'][resource_hash][key_hash]['logged_on']
        return sorted(dates)[0]

    def date_resource_last_collected(self, resource_hash):
        dates = self.concat_all_dates_resource_logged(resource_hash)
        return sorted(dates, reverse=True)[0]

    def date_resource_last_collected_from_key(self, resource_hash, key_hash):
        dates = self.mappings['resource'][resource_hash][key_hash]['logged_on']
        return sorted(dates, reverse=True)[0]

    def map_keys_to_organisations(self):
        self.mappings['organisation'] = {}
        idx = self.index
        for k in self.index['key']:
            for org in self.index['key'][k]["organisation"]:
                self.mappings["organisation"].setdefault(org, {"key": []})
                self.mappings["organisation"][org]["key"].append(k)


    def orgs_with_more_than_x_links(self, x=1, active=False):
        return [org for org in self.mappings['organisation'] if len(self.mappings['organisation'][org]['key']) > x]


    # returns dict
    #   {
    #       'count': {'organisation': [org, org, org]}
    #   }
    def orgs_by_no_links(self):
        counts = {}
        for org in self.mappings['organisation']:
            no_of_links = len(self.mappings['organisation'][org]['key'])
            counts.setdefault(no_of_links, {"organisation": []})
            counts[no_of_links]["organisation"].append(org)
        return counts


    def key_lifespan(self, key_hash):
        f = self.date_key_first_collected(key_hash)
        l = self.date_key_last_collected(key_hash)
        return days_between(f, l)

    def keys_by_age(self, reverse=False):
        timespans = [(k, self.key_lifespan(k)) for k in self.mappings['key'] if len(self.get_key_log(k)) > 0]
        return sorted(timespans, key=lambda tup: tup[1], reverse=reverse)

    def resource_lifespan(self, resource_hash):
        f = self.date_resource_first_collected(resource_hash)
        l = self.date_resource_last_collected(resource_hash)
        return days_between(f, l) + 1

    def resources_by_age(self, reverse=False):
        timespans = [(k, self.resource_lifespan(k)) for k in self.mappings['resource']]
        return sorted(timespans, key=lambda tup: tup[1], reverse=reverse)

    def print_resource_mapping(self):
        for r in self.mappings['resource']:
            if len(self.get_keys_for_resource(r)) > 1:
                #print(f"{r} maps to {len(self.get_keys_for_resource(r))} keys")
                print(f"Resource: {r}")
                for k in self.get_keys_for_resource(r):
                    print(f"-- key: {self.index['key'][k]['url']} first {self.date_resource_first_collected_from_key(r, k)} last {self.date_resource_last_collected_from_key(r, k)}")

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

    def generate_day_summary(self, daystr):
        fetched_on_day = 0
        status_index = {}

        for k in self.index['key']:
            if self.if_fetched_on_date(self.index['key'][k]['log'], daystr):
                fetched_on_day = fetched_on_day + 1
                if 'status' in self.index['key'][k]['log'][daystr].keys():
                    status = self.index['key'][k]['log'][daystr]['status']
                else:
                    status = self.index['key'][k]['log'][daystr]['exception']
                status_index.setdefault(status, {"key": []})
                status_index[status]["key"].append(k)

        return {
            "fetch_attempts": fetched_on_day,
            "statuses": status_index
        }

    def generate_today_summary(self):
        today = datetime.datetime.today().date().strftime('%Y-%m-%d')
        return self.print_day_summary(today)


    def resource_logged_for_day(self, log, daystr):
        if daystr in log and 'resource' in log[daystr]:
            return True
        return False


    def new_resources(self, daystr):
        changes = {}
        for link in self.index['key']:
            log = self.index['key'][link]['log']
            if self.if_fetched_on_date(log, daystr):
                if self.resource_logged_for_day(log, daystr) and self.resource_logged_for_day(log, previous_day(daystr)):
                    if log[daystr]['resource'] != log[previous_day(daystr)]['resource']:
                        changes[link] = (log[previous_day(daystr)]['resource'], log[daystr]['resource'])
        return changes

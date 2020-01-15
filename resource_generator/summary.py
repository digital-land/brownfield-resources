import datetime
import pprint
from resource_generator.collection import CollectionIndex


# create index mappings
ind = CollectionIndex()


def readable_day_summary(summary):
    print(f'Attempted to fetch {summary["fetch_attempts"]} files.\n')

    print("Results:", "\n--------")
    for k in summary['statuses'].keys():
        print(f'* {len(summary["statuses"][k]["key"])} {k}')

    if '404' in summary['statuses'].keys():
        print(f'\nLinks 404-ing are:', '\n------------------')
        for k in summary["statuses"]["404"]["key"]:
            print(f'* {ind.get_key(k)["url"]}')



def print_day_summary(daystr="today"):

    if daystr == 'today':
        daystr = datetime.datetime.today().date().strftime('%Y-%m-%d')

    print(f'On {daystr} the collector:', "\n===========================\n")

    readable_day_summary(ind.generate_day_summary(daystr))
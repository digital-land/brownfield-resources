import os

from resource_generator.collection import previous_day

def extract_file_name(file):
    base = os.path.basename(file)
    return os.path.splitext(base)[0]


def day_strs_between(start_date, end_date):
    day_strs = []

    day_str = end_date
    day_before_start = previous_day(start_date)

    while day_str != day_before_start:
        day_strs.append(day_str)
        day_str = previous_day(day_str)

    return day_strs

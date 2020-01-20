
# takes a string, chars to strip off, chars to add, the count
def pluralise(str, str_off, str_on, count):
    strip_count = -1*len(str_off) if len(str_off) > 0 else len(str)
    if count > 1:
        return str[:strip_count]+str_on
    else:
        return str


# takes a count and works out what colour heat map should show
# To do: make response dynamic
def colour_for_count(count):
    if count == 0:
        return "#ebedf0"
    elif count == 1:
        return "#6fa4d1"
    elif count == 2:
        return "#468ac4"
    elif count > 2:
        return "#1d70b8"


def org_dl_url(org_id):
    url_base = "https://digital-land.github.io/organisation/"
    return url_base + org_id.replace(":", "/")
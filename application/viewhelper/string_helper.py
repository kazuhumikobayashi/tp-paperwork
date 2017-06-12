from markupsafe import Markup


def filter_suppress_none(val):
    if val is not None:
        return val
    else:
        return ''


def number_with_commas(val):
    if val is not None:
        return "{:,}".format(val)
    else:
        return ''


def with_yen(val):
    if val:
        return Markup("&yen{}".format(val))
    else:
        return ''

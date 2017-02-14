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

import locale


def datetime_format(value, format='%H:%M / %d-%m-%Y'):
    if value is not None:
        locale.setlocale(locale.LC_ALL, '')
        return value.strftime(format)
    else:
        return ''

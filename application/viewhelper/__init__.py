from application.viewhelper.date_helper import datetime_format
from application.viewhelper.string_helper import filter_suppress_none, number_with_commas


def my_filter(app):
    app.jinja_env.filters['datetime_format'] = datetime_format
    app.jinja_env.filters['filter_suppress_none'] = filter_suppress_none
    app.jinja_env.filters['number_with_commas'] = number_with_commas

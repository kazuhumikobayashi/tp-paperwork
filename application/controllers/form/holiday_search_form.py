from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import validators, SelectField

year = datetime.today().year
last_year = str(year-1)
this_year = str(year)
next_year = str(year+1)


class HolidaySearchForm(FlaskForm):
    year = SelectField('年', [validators.optional()],
                       choices=[("", ""), (last_year, last_year + "年"),
                                (this_year, this_year + "年"), (next_year, next_year + "年")],
                       default=this_year,
                       render_kw={"data-placeholder": "年", "data-minimum-results-for-search": "Infinity"})

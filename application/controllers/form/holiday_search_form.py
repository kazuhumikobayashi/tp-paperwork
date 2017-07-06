from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import validators, SelectField


class HolidaySearchForm(FlaskForm):
    _year = datetime.today().year
    _last_year = str(_year - 1)
    _this_year = str(_year)
    _next_year = str(_year + 1)

    year = SelectField('年', [validators.optional()],
                       choices=[("", ""), (_last_year, _last_year + "年"),
                                (_this_year, _this_year + "年"), (_next_year, _next_year + "年")],
                       default=_this_year,
                       render_kw={"title": "年"})

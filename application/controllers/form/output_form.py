from flask_wtf import FlaskForm
from wtforms import SelectField, validators

from application.controllers.form.fields import BeginningOfMonthField
from application.controllers.form.validators import DataRequired
from application.domain.model.immutables.output_type import OutputType


class OutputForm(FlaskForm):
    output_report = SelectField('出力帳票選択',
                                [DataRequired()],
                                choices=OutputType.get_type_for_select(),
                                render_kw={"title": "出力帳票選択"})
    month = BeginningOfMonthField('年月', [validators.optional()], format='%Y/%m', render_kw={"autocomplete": "off"})

from flask_wtf import FlaskForm

from application.controllers.form.fields import IntegerField, DecimalField, DateField
from application.controllers.form.validators import DataRequired, InputRequired


class TaxForm(FlaskForm):
    id = IntegerField('Id')
    start_date = DateField('適用開始年月日', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    end_date = DateField('適用終了年月日', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    tax_rate = DecimalField('消費税率', [InputRequired()])

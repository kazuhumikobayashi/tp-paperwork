from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import DataRequired, InputRequired


class AssignedMemberForm(FlaskForm):
    project_id = HiddenField('プロジェクトID')
    engineer_id = SelectField('技術者', [DataRequired()])
    sales_unit_price = IntegerField('売単価', [InputRequired()])
    payment_unit_price = IntegerField('支払い単価', [InputRequired()])
    start_date = DateField('開始年月日', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    end_date = DateField('終了年月日', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})

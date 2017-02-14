from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField, TextAreaField, StringField, DateField

from application.controllers.form.fields import IntegerField, DecimalField
from application.controllers.form.validators import DataRequired, Length


class EngineerActualResultForm(FlaskForm):
    project_id = HiddenField('プロジェクトID')
    result_month = DateField('実績')
    engineer_id = SelectField('技術者', render_kw={"disabled": "disabled"})
    fixed_flg = SelectField('請求固定フラグ', [DataRequired()], choices=[('', ''), ('1', '請求固定'), ('2', '精算あり')],
                            render_kw={"data-minimum-results-for-search": "Infinity"})
    working_hours = DecimalField('実稼働時間')
    adjustment_hours = DecimalField('過不足時間')
    billing_amount = IntegerField('基本請求金額')
    billing_adjustment_amount = IntegerField('請求過不足金額')
    payment_amount = IntegerField('支払金額')
    payment_adjustment_amount = IntegerField('支払過不足金額')
    carfare = IntegerField('交通費')
    remarks = TextAreaField('備考', [Length(max=1024)])

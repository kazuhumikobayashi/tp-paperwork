from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, StringField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length


class ProjectMonthForm(FlaskForm):
    project_id = HiddenField('プロジェクトID')
    client_billing_no = StringField('顧客請求書No')
    billing_confirmation_money = IntegerField('請求確定金額（請求明細金額の合計）', render_kw={'disabled': 'disabled'})
    billing_transportation = IntegerField('請求交通費等（請求明細交通費等の合計）', render_kw={'disabled': 'disabled'})
    deposit_date = DateField('入金予定日', format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    remarks = TextAreaField('備考', [Length(max=1024)])
    project_month = DateField('プロジェクト年月', format='%Y/%m/%d')

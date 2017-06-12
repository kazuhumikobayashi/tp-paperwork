from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, StringField
from wtforms.validators import DataRequired

from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import Length


class BillingForm(FlaskForm):
    billing_content = StringField('請求明細内容（必須）', [DataRequired()])
    billing_amount = StringField('請求明細数量')
    billing_confirmation_money = IntegerField('請求明細金額（必須）', [DataRequired()])
    billing_transportation = IntegerField('請求明細交通費等')
    remarks = TextAreaField('備考', [Length(max=1024)])

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField

from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import Length, DataRequired, InputRequired


class ProjectBillingForm(FlaskForm):
    billing_content = StringField('請求明細内容（必須）', [DataRequired(), Length(max=128)])
    billing_amount = StringField('請求明細数量', [Length(max=128)], filters=[lambda x: x or None])
    billing_confirmation_money = IntegerField('請求明細金額（必須）', [InputRequired()])
    billing_transportation = IntegerField('請求明細交通費等')
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])

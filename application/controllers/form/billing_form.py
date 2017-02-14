from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField, TextAreaField, StringField, DateField
from wtforms.validators import Optional

from application.const import get_billing_status_for_select
from application.controllers.form.fields import IntegerField, DecimalField
from application.controllers.form.validators import DataRequired, Length


class BillingForm(FlaskForm):
    project_id = HiddenField('プロジェクトID')
    billing_month = DateField('請求')
    billing_amount = IntegerField('基本請求金額')
    billing_adjustment_amount = IntegerField('請求過不足金額')
    tax = IntegerField('消費税')
    carfare = IntegerField('交通費')
    scheduled_billing_date = DateField('請求予定日', [Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    billing_date = DateField('請求日', [Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    bill_output_date = DateField('請求書出力日', [Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    scheduled_payment_date = DateField('支払予定日', [Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    payment_date = DateField('支払日', [Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    status = SelectField('ステータス', [Optional()], choices=get_billing_status_for_select(),
                         filters=[lambda x: x or None],
                         render_kw={"data-minimum-results-for-search": "Infinity"})
    remarks = TextAreaField('備考', [Optional(), Length(max=1024)], filters=[lambda x: x or None])

from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField, StringField, SelectField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length


class OrderRemarksForm(FlaskForm):
    order_no = StringField('注文番号', [validators.optional(), Length(max=64)], filters=[lambda x: x or None])
    order_amount = IntegerField('注文金額')
    contents = TextAreaField('作業内容', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    responsible_person = TextAreaField('作業責任者', [validators.optional(), Length(max=128)], filters=[lambda x: x or None])
    subcontractor = TextAreaField('再委託先', [validators.optional(), Length(max=128)], filters=[lambda x: x or None])
    scope = TextAreaField('委託範囲', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    work_place = TextAreaField('作業場所', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    delivery_place = TextAreaField('納品場所', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    deliverables = TextAreaField('納品物', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    inspection_date = DateField('検査完了日', [validators.optional()], filters=[lambda x: x or None], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    payment_terms= TextAreaField('支払い条件', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    billing_company_id = SelectField('請求先', [validators.optional()], filters=[lambda x: x or None])
    remarks = TextAreaField('備考', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])

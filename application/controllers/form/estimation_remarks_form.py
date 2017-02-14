from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField

from application.controllers.form.fields import DateField
from application.controllers.form.validators import Length


class EstimationRemarksForm(FlaskForm):
    scope = TextAreaField('委託範囲', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    contents = TextAreaField('委託内容', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    deliverables = TextAreaField('納品物', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    delivery_place = TextAreaField('納品場所', [validators.optional(), Length(max=1024)], filters=[lambda x: x or None])
    inspection_date = DateField('検査完了日', [validators.optional()], filters=[lambda x: x or None], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    responsible_person = TextAreaField('作業責任者', [validators.optional(), Length(max=128)], filters=[lambda x: x or None])
    quality_control = TextAreaField('品質管理担当者', [validators.optional(), Length(max=128)], filters=[lambda x: x or None])
    subcontractor = TextAreaField('再委託先', [validators.optional(), Length(max=128)], filters=[lambda x: x or None])

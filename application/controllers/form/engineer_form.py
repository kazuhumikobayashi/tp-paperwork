from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectField, SelectMultipleField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired


class EngineerForm(FlaskForm):
    id = IntegerField('Id')
    start_date = DateField('適用開始年月日', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    end_date = DateField('適用終了年月日', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    engineer_name = StringField('技術者名', [Length(max=128)])
    engineer_name_kana = StringField('技術者名（カナ）', [Length(max=128)], filters=[lambda x: x or None])
    company_id = SelectField('会社', [validators.optional()], filters=[lambda x: x or None])
    remarks = StringField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    skill = SelectMultipleField('スキル', [Length(max=2048)], coerce=int)
    business_category = SelectMultipleField('業種', [Length(max=2048)], coerce=int)

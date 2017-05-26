from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectField, SelectMultipleField, \
    RadioField

from application.const import GENDER
from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired


class EngineerForm(FlaskForm):
    id = IntegerField('Id')
    engineer_name = StringField('技術者名称（必須）', [Length(max=128), DataRequired()])
    engineer_name_kana = StringField('技術者名称カナ', [Length(max=128)])
    birthday = DateField('生年月日',
                         [validators.optional()],
                         format='%Y/%m/%d',
                         render_kw={"autocomplete": "off"})
    gender = RadioField('性別',
                        [validators.optional()],
                        choices=GENDER,
                        filters=[lambda x: x or None])
    company_id = SelectField('所属会社（必須）', filters=[lambda x: x or None])
    business_category = SelectMultipleField(
        '業種', [Length(max=2048)], coerce=int)
    skill = SelectMultipleField('スキル', [Length(max=2048)], coerce=int)

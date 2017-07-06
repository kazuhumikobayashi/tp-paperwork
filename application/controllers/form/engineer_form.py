from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectField, SelectMultipleField

from application.controllers.form.fields import IntegerField, DateField, RadioField
from application.controllers.form.validators import Length, DataRequired
from application.domain.model.immutables.gender import Gender


class EngineerForm(FlaskForm):
    id = IntegerField('Id')
    engineer_name = StringField('技術者名称（必須）', [Length(max=128), DataRequired()])
    engineer_name_kana = StringField('技術者名称カナ', [Length(max=128)])
    birthday = DateField('生年月日',
                         [validators.optional()],
                         format='%Y/%m/%d',
                         render_kw={"autocomplete": "off"})
    gender = RadioField('性別',
                        choices=Gender.get_gender_for_radio())
    company_id = SelectField('所属会社（必須）', [DataRequired()],
                             render_kw={"title": "所属会社（必須）",
                                        "data-size": "8",
                                        "data-live-search": "true"})
    business_category = SelectMultipleField('業種', [Length(max=2048)], coerce=int,
                                            render_kw={"title": "業種（複数選択）",
                                                       "data-size": "8",
                                                       "data-live-search": "true",
                                                       "data-actions-box": "true"})
    skill = SelectMultipleField('スキル', [Length(max=2048)], coerce=int,
                                render_kw={"title": "スキル（複数選択）",
                                           "data-size": "8",
                                           "data-live-search": "true",
                                           "data-actions-box": "true"})

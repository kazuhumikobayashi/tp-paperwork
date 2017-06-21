from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.controllers.form.fields import CheckboxField


class EngineerSearchForm(FlaskForm):
    engineer_name = StringField('技術者名称', [validators.optional()])
    company_id = SelectMultipleField('所属会社', [validators.optional()],
                                     render_kw={"data-placeholder": "所属会社（複数選択）"})
    contract_engineer_is_checked = CheckboxField('',
                                                 [validators.optional()],
                                                 choices=[('1', '契約終了している技術者を省く')],
                                                 default='1')
    business_category_id = SelectMultipleField('業種', [validators.optional()],
                                               render_kw={"data-placeholder": "業種（複数選択）"})
    skill_id = SelectMultipleField('スキル', [validators.optional()],
                                   render_kw={"data-placeholder": "スキル（複数選択）"})

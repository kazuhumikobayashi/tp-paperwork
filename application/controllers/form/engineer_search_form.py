from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, DateField, SelectField, SelectMultipleField


class EngineerSearchForm(FlaskForm):
    engineer_name = StringField('技術者名', [validators.optional()])
    skill_id = SelectMultipleField('スキル', [validators.optional()],
                                   render_kw={"data-placeholder": "スキルを選択してください"})
    business_category_id = SelectMultipleField('業種', [validators.optional()],
                                   render_kw={"data-placeholder": "業種を選択してください"})
    company_id = SelectMultipleField('所属会社', [validators.optional()],
                                     render_kw={"data-placeholder": "所属会社を選択してください"})

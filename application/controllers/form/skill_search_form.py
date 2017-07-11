from flask_wtf import FlaskForm
from wtforms import validators, StringField


class SkillSearchForm(FlaskForm):
    skill_name = StringField('スキル', [validators.optional()])

from flask_wtf import FlaskForm
from wtforms import validators, StringField


class BusinessCategorySearchForm(FlaskForm):
    business_category_name = StringField('業種', [validators.optional()])

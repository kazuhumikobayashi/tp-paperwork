from flask_wtf import FlaskForm
from wtforms import validators, StringField


class DepartmentSearchForm(FlaskForm):
    group_name = StringField('本部名称', [validators.optional()])
    department_name = StringField('部署名称', [validators.optional()])

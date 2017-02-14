from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

from application.controllers.form.validators import Length, DataRequired


class DepartmentForm(FlaskForm):
    id = IntegerField('Id')
    department_code = StringField('部署コード', [DataRequired(), Length(max=32)])
    department_name = StringField('部署名', [DataRequired(), Length(max=128)])

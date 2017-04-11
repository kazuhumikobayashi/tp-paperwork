from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

from application.controllers.form.validators import Length, DataRequired


class DepartmentForm(FlaskForm):
    id = IntegerField('Id')
    department_name = StringField('部署名', [DataRequired(), Length(max=128)])

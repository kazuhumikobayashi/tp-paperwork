from flask_wtf import FlaskForm
from wtforms import StringField

from application.controllers.form.validators import Length, DataRequired


class ProjectCreateForm(FlaskForm):
    project_name = StringField('プロジェクト名（必須）',
                               [DataRequired(),
                                Length(max=128)])

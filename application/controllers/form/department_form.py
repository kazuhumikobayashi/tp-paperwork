from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField
from wtforms import ValidationError

from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.department_repository import DepartmentRepository

repository = DepartmentRepository()


class DepartmentForm(FlaskForm):
    id = IntegerField('Id')
    group_name = StringField('本部名称（必須）', [DataRequired(), Length(max=128)])
    department_name = StringField('部署名称（必須）', [DataRequired(), Length(max=128)])
    updated_user = StringField('更新者')
    updated_at = DateTimeField('更新日')

    def validate_department_name(self, field):
        skill = repository.find_by_department_name(field.data)
        if skill and skill.id != self.id.data:
            raise ValidationError('同じ名称の部署が既に登録されています。')

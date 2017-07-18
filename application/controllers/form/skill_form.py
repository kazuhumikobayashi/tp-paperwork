from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms import ValidationError

from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.skill_repository import SkillRepository

repository = SkillRepository()


class SkillForm(FlaskForm):
    id = IntegerField('Id')
    skill_name = StringField('スキル（必須）', [DataRequired(), Length(max=32)])
    updated_user = StringField('更新者')
    updated_at = DateTimeField('更新日')

    def validate_skill_name(self, field):
        skill = repository.find_by_name(field.data)
        if skill and skill.id != self.id.data:
            raise ValidationError('同じ名称のスキルが既に登録されています。')

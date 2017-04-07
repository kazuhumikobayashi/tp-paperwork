from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import validators, StringField, IntegerField

from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.user_repository import UserRepository

repository = UserRepository()


class UserForm(FlaskForm):
    id = IntegerField('Id')
    shain_number = StringField('社員番号', [Length(max=32)])
    user_name = StringField('ユーザー名', [DataRequired(), Length(max=128)])

    def validate_shain_number(self, field):
        user = repository.find_by_shain_number(shain_number=field.data)
        if user and user.id != self.id.data:
            raise ValidationError('この社員番号は既に登録されています。')
        if self.id.data and (field.data is None or field.data == ''):
            raise ValidationError('社員番号は必須です。')

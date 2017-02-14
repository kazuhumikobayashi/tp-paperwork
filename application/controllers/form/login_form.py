from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms import ValidationError

from application.controllers.form.validators import DataRequired
from application.domain.repository.user_repository import UserRepository

repository = UserRepository()


class LoginForm(FlaskForm):
    shain_number = StringField('社員番号', [DataRequired()])
    password = PasswordField('パスワード', [DataRequired()])

    def validate_password(self, field):
        user = repository.find_by_shain_number(self.shain_number.data)
        if user and not user.can_login(field.data):
            raise ValidationError('社員番号またはパスワードが違います。')

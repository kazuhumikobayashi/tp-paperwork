from flask import session
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import ValidationError
from wtforms.validators import EqualTo

from application.controllers.form.validators import DataRequired
from application.domain.repository.user_repository import UserRepository

repository = UserRepository()


class PwChangeForm(FlaskForm):
    password = PasswordField('現在のパスワード', [DataRequired()])
    new_password = PasswordField('新しいパスワード',[DataRequired()])
    new_password_confirmation = PasswordField('新しいパスワード（確認）',
                                              [DataRequired(),
                                               EqualTo('new_password',
                                                       message='新しいパスワードと新しいパスワード（確認）が一致していません')])

    def validate_password(self, field):
        user = repository.find_by_id(session['user']['id'])
        if user and not user.can_login(field.data):
            raise ValidationError('現在のパスワードが違います。')

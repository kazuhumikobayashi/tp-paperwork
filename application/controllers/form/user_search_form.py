from flask_wtf import FlaskForm
from wtforms import validators, StringField


class UserSearchForm(FlaskForm):
    user_name = StringField('ユーザー名称', [validators.optional()])
    shain_number = StringField('社員番号', [validators.optional()])

from flask_wtf import FlaskForm
from wtforms import DateTimeField
from wtforms import StringField, IntegerField

from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.bank_repository import BankRepository

repository = BankRepository()


class BankForm(FlaskForm):
    id = IntegerField('Id')
    bank_name = StringField('銀行名称（必須）', [DataRequired(), Length(max=32)])
    text_for_document = StringField('書類提出用文言名称（必須）', [DataRequired(), Length(max=128)])
    updated_user = StringField('更新者')
    updated_at = DateTimeField('更新日')

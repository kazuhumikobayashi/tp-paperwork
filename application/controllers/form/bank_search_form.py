from flask_wtf import FlaskForm
from wtforms import validators, StringField


class BankSearchForm(FlaskForm):
    bank_name = StringField('銀行名称', [validators.optional()])
    text_for_document = StringField('書類提出用文言名称', [validators.optional()])

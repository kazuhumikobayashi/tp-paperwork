from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectField

from application.controllers.form.validators import DataRequired, Length


class DestinationForm(FlaskForm):
    company_id = SelectField('会社', [DataRequired()],
                             render_kw={"data-placeholder": "会社を選択してください"})
    destination_name = StringField('宛先名', [DataRequired(), Length(max=128)])
    destination_department = StringField('宛先部署', [validators.optional(), Length(max=128)])

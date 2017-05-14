from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField


class DestinationSearchForm(FlaskForm):
    company_id = SelectMultipleField('会社', [validators.optional()],
                                     render_kw={"data-placeholder": "会社を選択してください"})
    destination_name = StringField('宛先名')
    destination_department = StringField('宛先部署')

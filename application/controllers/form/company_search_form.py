from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField


class CompanySearchForm(FlaskForm):
    company_name = StringField('会社名、会社名称カナ、会社略称（部分一致）', [validators.optional()])
    client_flag_id = SelectMultipleField('顧客フラグ', [validators.optional()],
                                         render_kw={"data-placeholder": "顧客フラグ（複数選択）"})
    bank_id = SelectMultipleField('振込先銀行', [validators.optional()],
                                  render_kw={"data-placeholder": "振込先銀行（複数選択）"})

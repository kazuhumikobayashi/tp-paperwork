from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.controllers.form.fields import CheckboxField

from application.domain.model.immutables.input_flag import InputFlag


class SearchBillingForm(FlaskForm):
    today = datetime.today().date()
    first_day = today.replace(day=1)
    last_day = first_day + relativedelta(months=1, days=-1)
    
    project_name = StringField('プロジェクト名称', [validators.optional()])
    billing_input_flag = CheckboxField('請求ステータス', choices=InputFlag.get_billing_flag_for_radio())
    deposit_input_flag = CheckboxField('入金ステータス', choices=InputFlag.get_deposit_flag_for_radio())
    end_user_company_id = SelectMultipleField('エンドユーザー', [validators.optional()],
                                              render_kw={"data-placeholder": "エンドユーザ（複数選択）"})
    client_company_id = SelectMultipleField('顧客', [validators.optional()],
                                            render_kw={"data-placeholder": "顧客会社（複数選択）"})
    recorded_department_id = SelectMultipleField('計上部署',
                                                 render_kw={"data-placeholder": "計上部署（複数選択）"})
    deposit_date_from = StringField('入金予定日(From)', [validators.optional()],
                                    default=first_day.strftime("%Y/%m/%d"),
                                    render_kw={"autocomplete": "off"})
    deposit_date_to = StringField('入金予定日(To)', [validators.optional()],
                                  default=last_day.strftime("%Y/%m/%d"),
                                  render_kw={"autocomplete": "off"})

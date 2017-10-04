from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.controllers.form.fields import CheckboxField, SelectMultiFieldWithSubtext

from application.domain.model.immutables.input_flag import InputFlag


class SearchBillingForm(FlaskForm):
    today = datetime.today().date()
    first_day = today.replace(day=1)
    last_day = first_day + relativedelta(months=1, days=-1)
    
    project_name = StringField('プロジェクト名称', [validators.optional()])
    estimation_no = StringField('見積No', [validators.optional()])
    billing_input_flag = CheckboxField('請求ステータス', choices=InputFlag.get_billing_flag_for_radio())
    deposit_input_flag = CheckboxField('入金ステータス', choices=InputFlag.get_deposit_flag_for_radio())
    end_user_company_id = SelectMultiFieldWithSubtext('エンドユーザー', [validators.optional()],
                                                      render_kw={"title": "エンドユーザー（複数選択）",
                                                                 "data-live-search": "true",
                                                                 "data-size": "8",
                                                                 "data-actions-box": "true",
                                                                 "data-selected-text-format": "count > 3"})
    client_company_id = SelectMultiFieldWithSubtext('顧客', [validators.optional()],
                                                    render_kw={"title": "顧客会社（複数選択）",
                                                               "data-live-search": "true",
                                                               "data-size": "8",
                                                               "data-actions-box": "true",
                                                               "data-selected-text-format": "count > 3"})
    recorded_department_id = SelectMultipleField('計上部署',
                                                 render_kw={"title": "計上部署（複数選択）",
                                                            "data-size": "8",
                                                            "data-actions-box": "true",
                                                            "data-selected-text-format": "count > 3"})
    deposit_date_from = StringField('入金予定日(From)', [validators.optional()],
                                    default=first_day.strftime("%Y/%m/%d"),
                                    render_kw={"autocomplete": "off"})
    deposit_date_to = StringField('入金予定日(To)', [validators.optional()],
                                  default=last_day.strftime("%Y/%m/%d"),
                                  render_kw={"autocomplete": "off"})

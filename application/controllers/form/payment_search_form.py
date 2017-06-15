from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.controllers.form.fields import RadioField
from application.domain.model.immutables.input_flag import InputFlag


class PaymentSearchForm(FlaskForm):
    today = datetime.today().date()
    first_day = today.replace(day=1)
    last_day = first_day + relativedelta(months=1, days=-1)

    project_name = StringField('プロジェクト名', [validators.optional()])
    input_flag = RadioField('支払ステータス', choices=InputFlag.get_flag_for_radio())
    end_user_company_id = SelectMultipleField('エンドユーザー', [validators.optional()],
                                              render_kw={"data-placeholder": "エンドユーザーを選択してください"})
    client_company_id = SelectMultipleField('顧客', [validators.optional()],
                                            render_kw={"data-placeholder": "顧客会社を選択してください"})
    recorded_department_id = SelectMultipleField('計上部署',
                                                 render_kw={"data-placeholder": "計上部署を選択してください"})
    engineer_name = StringField('技術者名', [validators.optional()])
    payment_expected_date_from = StringField('支払予定日(From)', [validators.optional()],
                                             default=first_day.strftime("%Y/%m/%d"),
                                             render_kw={"autocomplete": "off"})
    payment_expected_date_to = StringField('支払予定日(To)', [validators.optional()],
                                           default=last_day.strftime("%Y/%m/%d"),
                                           render_kw={"autocomplete": "off"})

from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.controllers.form.fields import CheckboxField
from application.domain.model.immutables.input_flag import InputFlag


class SearchResultForm(FlaskForm):
    today = datetime.today().date()
    first_day = today.replace(day=1)
    last_first_day = first_day + relativedelta(months=-1)
    last_day = first_day + relativedelta(months=1, days=-1)
    
    project_name = StringField('プロジェクト名称', [validators.optional()])
    result_input_flag = CheckboxField('実績ステータス', choices=InputFlag.get_result_flag_for_radio())
    end_user_company_id = SelectMultipleField('エンドユーザー', [validators.optional()],
                                              render_kw={"data-placeholder": "エンドユーザー（複数選択）"})
    client_company_id = SelectMultipleField('顧客', [validators.optional()],
                                            render_kw={"data-placeholder": "顧客会社（複数選択）"})
    recorded_department_id = SelectMultipleField('計上部署',
                                                 render_kw={"data-placeholder": "計上部署（複数選択）"})
    engineer_name = StringField('技術者名称', [validators.optional()])
    result_month_from = StringField('実績年月（From）', [validators.optional()],
                                    default=last_first_day.strftime('%Y/%m'),
                                    render_kw={"autocomplete": "off"})
    result_month_to = StringField('実績年月（To）', [validators.optional()],
                                  default=last_day.strftime('%Y/%m'),
                                  render_kw={"autocomplete": "off"})

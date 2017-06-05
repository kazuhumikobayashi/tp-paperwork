from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.domain.model.immutables.status import Status


class ProjectSearchForm(FlaskForm):
    project_name = StringField('プロジェクト名', [validators.optional()])
    status = SelectMultipleField('契約ステータス',
                                 choices=Status.get_status_for_select(),
                                 render_kw={"data-placeholder": "契約ステータスを選択してください"})
    end_user_company_id = SelectMultipleField('エンドユーザー', [validators.optional()],
                                              render_kw={"data-placeholder": "エンドユーザーを選択してください"})
    client_company_id = SelectMultipleField('顧客', [validators.optional()],
                                            render_kw={"data-placeholder": "顧客会社を選択してください"})
    recorded_department_id = SelectMultipleField('計上部署',
                                                 render_kw={"data-placeholder": "計上部署を選択してください"})
    start_date = StringField('プロジェクト開始日', [validators.optional()], render_kw={"autocomplete": "off"})
    end_date = StringField('プロジェクト終了日', [validators.optional()], render_kw={"autocomplete": "off"})

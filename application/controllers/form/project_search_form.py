from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField

from application.domain.model.immutables.status import Status


class ProjectSearchForm(FlaskForm):
    project_name = StringField('プロジェクト名', [validators.optional()])
    status = SelectMultipleField('契約ステータス',
                                 choices=Status.get_status_for_multi_select(),
                                 render_kw={"title": "契約ステータス（複数選択）",
                                            "data-size": "8",
                                            "data-actions-box": "true",
                                            "data-selected-text-format": "count > 3"})
    end_user_company_id = SelectMultipleField('エンドユーザー', [validators.optional()],
                                              render_kw={"title": "エンドユーザー（複数選択）",
                                                         "data-live-search": "true",
                                                         "data-size": "8",
                                                         "data-actions-box": "true",
                                                         "data-selected-text-format": "count > 3"})
    client_company_id = SelectMultipleField('顧客', [validators.optional()],
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
    start_date = StringField('プロジェクト開始日', [validators.optional()], render_kw={"autocomplete": "off"})
    end_date = StringField('プロジェクト終了日', [validators.optional()], render_kw={"autocomplete": "off"})

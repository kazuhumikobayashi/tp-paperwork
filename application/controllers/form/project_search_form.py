from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectMultipleField


class ProjectSearchForm(FlaskForm):
    start_date = StringField('開始日', [validators.optional()], render_kw={"autocomplete": "off"})
    end_date = StringField('終了日', [validators.optional()], render_kw={"autocomplete": "off"})
    project_name = StringField('プロジェクト名', [validators.optional()])
    end_user = StringField('エンドユーザー', [validators.optional()])
    client_company_id = SelectMultipleField('顧客', [validators.optional()],
                                            render_kw={"data-placeholder": "顧客会社を選択してください"})
    recorded_department_id = SelectMultipleField('計上部署',
                                                 render_kw={"data-placeholder": "計上部署を選択してください"})

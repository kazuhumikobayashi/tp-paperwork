from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms import ValidationError

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.project_repository import ProjectRepository

repository = ProjectRepository()


class ProjectForm(FlaskForm):
    id = IntegerField('プロジェクトコード')
    project_name = StringField('プロジェクト名',
                               [DataRequired(),
                                Length(max=128)])
    end_user = StringField('エンドユーザー', [Length(max=128)], filters=[lambda x: x or None])
    client_company_id = SelectField('顧客', [DataRequired()])
    start_date = DateField('プロジェクト開始年月日',
                           [DataRequired()],
                           format='%Y/%m/%d',
                           render_kw={"autocomplete": "off"})
    end_date = DateField('プロジェクト終了年月日',
                         [DataRequired()],
                         format='%Y/%m/%d',
                         render_kw={"autocomplete": "off"})
    recorded_department_id = SelectField('計上部署',
                                         [DataRequired()],
                                         render_kw={"data-minimum-results-for-search": "Infinity"})
    over_time_calculation_id = SelectField('残業計算', [DataRequired()],
                                           render_kw={"data-minimum-results-for-search": "Infinity"})
    contract_form_id = SelectField('契約形態', [Length(max=1)],
                                   filters=[lambda x: x or None],
                                   render_kw={"data-minimum-results-for-search": "Infinity"})
    estimation_no = StringField('見積No', [Length(max=64)])
    status_id = SelectField('ステータス',
                            [DataRequired(), Length(max=1)],
                            render_kw={"data-minimum-results-for-search": "Infinity"})
    billing_timing = SelectField('請求タイミング',
                                 [Length(max=1)],
                                 choices=[('', ''), ('1', '毎月'), ('2', '指定月')],
                                 filters=[lambda x: x or None],
                                 render_kw={"data-minimum-results-for-search": "Infinity"})
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    assigned_members = []
    engineer_actual_results = []

    def validate_estimation_no(self, field):
        project = repository.find_by_estimation_no(estimation_no=field.data)
        if project and project.id != self.id.data:
            raise ValidationError('この見積Noは既に登録されています。')

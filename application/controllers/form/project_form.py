from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectField, TextAreaField
from wtforms import ValidationError

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.project_repository import ProjectRepository
from application.const import FORMULA

repository = ProjectRepository()


class ProjectForm(FlaskForm):
    id = IntegerField('プロジェクトコード')
    project_name = StringField('プロジェクト名',
                               [DataRequired(),
                                Length(max=128)])
    end_user_company_id = SelectField('エンドユーザー', [DataRequired()])
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
                                           choices=FORMULA,
                                           render_kw={"data-minimum-results-for-search": "Infinity"})
    contract_form = SelectField('契約形態',
                                [validators.optional(), Length(max=128)],
                                choices=[('', ''),
                                         ('請負契約（一括契約）', '請負契約（一括契約）'),
                                         ('準委任契約', '準委任契約'),
                                         ('派遣契約', '派遣契約')],
                                filters=[lambda x: x or None],
                                render_kw={"data-minimum-results-for-search": "Infinity"})
    estimation_no = StringField('見積No', [Length(max=64)])
    status = SelectField('ステータス',
                         [validators.optional(), Length(max=128)],
                         choices=[('', ''),
                                  ('01:契約開始', '01:契約開始'),
                                  ('02:発注完了', '02:発注完了'),
                                  ('03:受注完了', '03:受注完了'),
                                  ('04:契約完了', '04:契約完了'),
                                  ('99:失注', '99:失注')],
                         filters=[lambda x: x or None],
                         render_kw={"data-minimum-results-for-search": "Infinity"})
    billing_timing = SelectField('請求タイミング',
                                 [validators.optional(), Length(max=128)],
                                 choices=[('', ''),
                                          ('契約期間末1回', '契約期間末1回'),
                                          ('その他（毎月・複数月）', 'その他（毎月・複数月）')],
                                 filters=[lambda x: x or None],
                                 render_kw={"data-minimum-results-for-search": "Infinity"})
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    assigned_members = []
    engineer_actual_results = []

    def validate_estimation_no(self, field):
        project = repository.find_by_estimation_no(estimation_no=field.data)
        if project and project.id != self.id.data:
            raise ValidationError('この見積Noは既に登録されています。')

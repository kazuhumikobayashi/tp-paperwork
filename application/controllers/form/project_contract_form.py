from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import validators, StringField, SelectField, TextAreaField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired, LessThan
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.repository.project_repository import ProjectRepository

repository = ProjectRepository()


class ProjectContractForm(FlaskForm):
    id = IntegerField('プロジェクトコード')
    project_name = StringField('プロジェクト名称（必須）', [DataRequired(), Length(max=128)])
    project_name_for_bp = StringField('BP向けプロジェクト名称', [Length(max=128)], filters=[lambda x: x or None])
    status = SelectField('契約ステータス（必須）',
                         [DataRequired()],
                         choices=Status.get_status_for_select(),
                         render_kw={"title": "契約ステータス（必須）"})
    recorded_department_id = SelectField('計上部署（必須）',
                                         [DataRequired()],
                                         render_kw={"title": "計上部署（必須）"})
    sales_person = StringField('営業担当者名称', [Length(max=128)], filters=[lambda x: x or None])
    estimation_no = StringField('見積No（必須）', [DataRequired(), Length(max=64)])
    end_user_company_id = SelectField('エンドユーザー（必須）', [DataRequired()],
                                      render_kw={"title": "エンドユーザー（必須）",
                                                 "data-live-search": "true",
                                                 "data-size": "8",
                                                 "data-actions-box": "true"})
    client_company_id = SelectField('顧客会社（必須）', [DataRequired()],
                                    render_kw={"title": "顧客会社（必須）",
                                               "data-live-search": "true",
                                               "data-size": "8",
                                               "data-actions-box": "true"})
    start_date = DateField('プロジェクト開始日（必須）',
                           [DataRequired(), LessThan('end_date')],
                           format='%Y/%m/%d',
                           render_kw={"autocomplete": "off"})
    end_date = DateField('プロジェクト終了日（必須）', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    contract_form = SelectField('契約形態（必須）',
                                [DataRequired()],
                                choices=Contract.get_type_for_select(),
                                render_kw={"title": "契約形態（必須）"})
    billing_timing = SelectField('請求タイミング（必須）',
                                 [DataRequired()],
                                 choices=BillingTiming.get_type_for_select(),
                                 render_kw={"title": "請求タイミング（必須）"})
    estimated_total_amount = IntegerField('見積金額合計',
                                          render_kw={"disabled": "disabled"})
    billing_site = IntegerField('入金サイト', render_kw={"disabled": "disabled"})
    billing_tax = SelectField('入金消費税区分',
                              [validators.Optional()],
                              choices=Tax.get_type_for_select(),
                              render_kw={"title": "入金消費税区分", "disabled": "disabled"})
    scope = TextAreaField('作業範囲', [Length(max=1024)], filters=[lambda x: x or None])
    contents = TextAreaField('作業内容', [Length(max=1024)], filters=[lambda x: x or None])
    working_place = StringField('作業場所', [Length(max=1024)], filters=[lambda x: x or None])
    delivery_place = StringField('納入場所', [Length(max=1024)], filters=[lambda x: x or None])
    deliverables = StringField('納品物', [Length(max=1024)], filters=[lambda x: x or None])
    inspection_date = DateField('検査完了日', format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    responsible_person = StringField('作業責任者', [Length(max=128)], filters=[lambda x: x or None])
    quality_control = StringField('品質管理担当者', [Length(max=128)], filters=[lambda x: x or None])
    subcontractor = StringField('再委託先', [Length(max=64)], filters=[lambda x: x or None])
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    client_order_no = StringField('顧客注文書No', [Length(max=64)], filters=[lambda x: x or None])

    def validate_estimation_no(self, field):
        project = repository.find_by_estimation_no(estimation_no=field.data)
        if project and project.id != self.id.data:
            raise ValidationError('この見積Noは既に登録されています。')

    def validate_status(self, field):
        if field.data == str(Status.done):
            project = repository.find_by_id(self.id.data)
            if not project.project_details:
                raise ValidationError('契約完了時には明細が必須です。')

from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import validators, StringField, SelectField, TextAreaField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.repository.project_repository import ProjectRepository

repository = ProjectRepository()


class ContractForm(FlaskForm):
    id = IntegerField('プロジェクトコード')
    project_name = StringField('プロジェクト名称', [DataRequired(), Length(max=128)])
    project_name_for_bp = StringField('BP向けプロジェクト名称', [Length(max=128)], filters=[lambda x: x or None])
    status = SelectField('契約ステータス',
                         choices=Status.get_status_for_select(),
                         render_kw={"data-minimum-results-for-search": "Infinity"})
    recorded_department_id = SelectField('計上部署（必須）',
                                         render_kw={"data-minimum-results-for-search": "Infinity"})
    sales_person = StringField('営業担当者名称', [Length(max=128)], filters=[lambda x: x or None])
    estimation_no = StringField('見積No（必須）', [DataRequired(), Length(max=64)])
    end_user_company_id = SelectField('エンドユーザー（必須）')
    client_company_id = SelectField('顧客会社（必須）')
    start_date = DateField('プロジェクト開始日（必須）', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    end_date = DateField('プロジェクト終了日（必須）', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    contract_form = SelectField('契約形態（必須）',
                                [Length(max=128)],
                                choices=Contract.get_type_for_select(),
                                render_kw={"data-minimum-results-for-search": "Infinity"})
    billing_timing = SelectField('請求タイミング（必須）',
                                 [Length(max=128)],
                                 choices=BillingTiming.get_type_for_select(),
                                 render_kw={"data-minimum-results-for-search": "Infinity"})
    estimated_total_amount = IntegerField('見積金額合計', filters=[lambda x: x or None])
    payment_site = IntegerField('入金サイト', filters=[lambda x: x or None])
    payment_tax = SelectField('入金消費税区分',
                              choices=Tax.get_type_for_select(),
                              render_kw={"data-minimum-results-for-search": "Infinity"})
    deposit_date = DateField('単月入金予定日', [validators.Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    scope = StringField('委託範囲', [Length(max=1024)], filters=[lambda x: x or None])
    contents = StringField('委託内容', [Length(max=1024)], filters=[lambda x: x or None])
    working_place = StringField('作業場所', [Length(max=1024)], filters=[lambda x: x or None])
    delivery_place = StringField('納入場所', [Length(max=1024)], filters=[lambda x: x or None])
    deliverables = StringField('納品物', [Length(max=1024)], filters=[lambda x: x or None])
    inspection_date = DateField('検査完了日', [validators.Optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    responsible_person = StringField('作業責任者', [Length(max=128)], filters=[lambda x: x or None])
    quality_control = StringField('品質管理担当者', [Length(max=128)], filters=[lambda x: x or None])
    subcontractor = StringField('再委託先', [Length(max=64)], filters=[lambda x: x or None])
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    client_order_no = StringField('顧客注文書No', [Length(max=64)], filters=[lambda x: x or None])

    def validate_estimation_no(self, field):
        project = repository.find_by_estimation_no(estimation_no=field.data)
        if project and project.id != self.id.data:
            raise ValidationError('この見積Noは既に登録されています。')

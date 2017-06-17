from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.contract_form import ContractForm
from application.controllers.form.project_detail_form import ProjectDetailForm
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.status import Status
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.engineer_history_service import EngineerHistoryService
from application.service.engineer_service import EngineerService
from application.service.project_detail_service import ProjectDetailService
from application.service.project_service import ProjectService

bp = Blueprint('project_contract', __name__, url_prefix='/project/contract')
project_service = ProjectService()
project_detail_service = ProjectDetailService()
engineer_service = EngineerService()
engineer_history_service = EngineerHistoryService()
department_service = DepartmentService()
company_service = CompanyService()


@bp.route('/<project_id>', methods=['GET', 'POST'])
def index(project_id=None):
    project = project_service.find_by_id(project_id)

    if project.id is None and project_id is not None:
        return abort(404)

    form = ContractForm(request.form, project)
    form.recorded_department_id.choices = department_service.find_all_for_select()
    form.client_company_id.choices = company_service.find_for_select_by_client_flag_id([ClientFlag.client.value])
    form.end_user_company_id.choices = company_service.find_for_select_by_client_flag_id([ClientFlag.end_user.value])

    if project.client_company_id:
        form.billing_site.data = project.client_company.billing_site
        form.billing_tax.data = str(project.client_company.billing_tax)

    if form.validate_on_submit():
        project.project_name = form.project_name.data
        project.project_name_for_bp = form.project_name_for_bp.data
        project.status = Status.parse(form.status.data)
        project.recorded_department_id = form.recorded_department_id.data
        project.sales_person = form.sales_person.data
        project.estimation_no = form.estimation_no.data
        project.end_user_company_id = form.end_user_company_id.data
        project.client_company_id = form.client_company_id.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.contract_form = Contract.parse(form.contract_form.data)
        project.billing_timing = BillingTiming.parse(form.billing_timing.data)
        project.estimated_total_amount = form.estimated_total_amount.data
        if form.deposit_date.data is None:
            project.client_company = company_service.find_by_id(form.client_company_id.data)
            project.deposit_date = project.get_deposit_date()
        else:
            project.deposit_date = form.deposit_date.data
        project.scope = form.scope.data
        project.contents = form.contents.data
        project.working_place = form.working_place.data
        project.delivery_place = form.delivery_place.data
        project.deliverables = form.deliverables.data
        project.inspection_date = form.inspection_date.data
        project.responsible_person = form.responsible_person.data
        project.quality_control = form.quality_control.data
        project.subcontractor = form.subcontractor.data
        project.remarks = form.remarks.data
        project.client_order_no = form.client_order_no.data

        project_service.save(project)
        flash('保存しました。')
        return redirect(url_for('.index', project_id=project.id))
    current_app.logger.debug(form.errors)

    return render_template('project/contract/index.html',
                           form=form,
                           project=project)


@bp.route('/detail/<project_detail_id>', methods=['GET', 'POST'])
def detail(project_detail_id=None):
    project_id = request.args.get('project_id')
    project_detail = project_detail_service.find_by_id(project_detail_id)

    if project_detail.id is None and project_detail_id is not None \
            or project_detail.project is None and project_id is None:
        return abort(404)

    form = ProjectDetailForm(request.form, project_detail)
    form.engineer_id.choices = engineer_service.find_all_for_select()

    # 新規作成時にはprojectを取得する。
    if project_id:
        project_detail.project = project_service.find_by_id(project_id)
    if form.engineer_id.data:
        project_detail.engineer = engineer_service.find_by_id(form.engineer_id.data)

    if form.detail_type.data == str(DetailType.engineer) and project_detail.engineer is not None:
        current_engineer_history = engineer_history_service.get_current_history(project_detail.engineer.id)

        form.company.data = project_detail.engineer.company.company_name
        form.payment_start_day.data = current_engineer_history.payment_start_day
        form.payment_end_day.data = current_engineer_history.payment_end_day
        form.payment_per_month.data = current_engineer_history.payment_per_month
        form.payment_rule.data = str(current_engineer_history.payment_rule)
        form.payment_bottom_base_hour.data = current_engineer_history.payment_bottom_base_hour
        form.payment_top_base_hour.data = current_engineer_history.payment_top_base_hour
        form.payment_free_base_hour.data = current_engineer_history.payment_free_base_hour
        form.payment_per_hour.data = current_engineer_history.payment_per_hour
        form.payment_per_bottom_hour.data = current_engineer_history.payment_per_bottom_hour
        form.payment_per_top_hour.data = current_engineer_history.payment_per_top_hour
        form.payment_fraction.data = current_engineer_history.payment_fraction
        form.payment_fraction_calculation1.data = str(current_engineer_history.payment_fraction_calculation1)
        form.payment_fraction_calculation2.data = str(current_engineer_history.payment_fraction_calculation2)

    if form.validate_on_submit():
        project_detail.project_id = project_detail.project.id
        project_detail.detail_type = DetailType.parse(form.detail_type.data)
        project_detail.work_name = form.work_name.data
        project_detail.engineer = project_detail.engineer
        project_detail.billing_money = form.billing_money.data
        project_detail.remarks = form.remarks.data
        project_detail.billing_start_day = form.billing_start_day.data
        project_detail.billing_end_day = form.billing_end_day.data
        project_detail.billing_per_month = form.billing_per_month.data
        project_detail.billing_rule = Rule.parse(form.billing_rule.data)
        project_detail.billing_bottom_base_hour = form.billing_bottom_base_hour.data
        project_detail.billing_top_base_hour = form.billing_top_base_hour.data
        project_detail.billing_free_base_hour = form.billing_free_base_hour.data
        project_detail.billing_per_hour = form.billing_per_hour.data
        project_detail.billing_per_bottom_hour = form.billing_per_bottom_hour.data
        project_detail.billing_per_top_hour = form.billing_per_top_hour.data
        project_detail.billing_fraction = form.billing_fraction.data
        project_detail.billing_fraction_calculation1 = form.billing_fraction_calculation1.data or None
        project_detail.billing_fraction_calculation2 = form.billing_fraction_calculation2.data or None
        project_detail.bp_order_no = form.bp_order_no.data
        project_detail.client_order_no_for_bp = form.client_order_no_for_bp.data

        project_detail_service.save(project_detail)
        flash('保存しました。')
        return redirect(url_for('.detail', project_detail_id=project_detail.id))

    current_app.logger.debug(form.errors)
    return render_template('project/contract/detail.html', form=form, project_detail=project_detail)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<project_detail_id>', methods=['GET'])
def delete(project_detail_id):
    project_detail = project_detail_service.find_by_id(project_detail_id)
    if project_detail.id is not None:
        project_id = project_detail.project_id
        project_detail_service.destroy(project_detail)
        flash('削除しました。')
        return redirect(url_for('.index', project_id=project_id))
    else:
        return redirect('/project')

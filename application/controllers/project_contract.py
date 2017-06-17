from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.contract_form import ContractForm
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.status import Status
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.project_service import ProjectService

bp = Blueprint('project_contract', __name__, url_prefix='/project/contract')
service = ProjectService()
department_service = DepartmentService()
company_service = CompanyService()


@bp.route('/<project_id>', methods=['GET', 'POST'])
def index(project_id=None):
    project = service.find_by_id(project_id)

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

        service.save(project)
        flash('保存しました。')
        return redirect(url_for('.index', project_id=project.id))
    current_app.logger.debug(form.errors)

    return render_template('project/contract/index.html',
                           form=form,
                           project=project)

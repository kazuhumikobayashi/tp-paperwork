from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.estimation_remarks_form import EstimationRemarksForm
from application.controllers.form.order_remarks_form import OrderRemarksForm
from application.controllers.form.project_create_form import ProjectCreateForm
from application.controllers.form.project_form import ProjectForm
from application.controllers.form.project_search_form import ProjectSearchForm
from application.domain.model.estimation_remarks import EstimationRemarks
from application.domain.model.order_remarks import OrderRemarks
from application.domain.model.project import Project
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.estimation_remarks_service import EstimationRemarksService
from application.service.order_remarks_service import OrderRemarksService
from application.service.project_service import ProjectService

bp = Blueprint('project', __name__, url_prefix='/project')
service = ProjectService()
department_service = DepartmentService()
company_service = CompanyService()
estimation_remarks_service = EstimationRemarksService()
order_remarks_service = OrderRemarksService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = ProjectSearchForm(request.values)
    form.client_company_id.choices = company_service.find_all_for_multi_select()
    form.end_user_company_id.choices = company_service.find_all_for_multi_select()
    form.recorded_department_id.choices = department_service.find_all_for_multi_select()
    pagination = service.find(page,
                              form.start_date.data,
                              form.end_date.data,
                              form.project_name.data,
                              form.end_user_company_id.data,
                              form.client_company_id.data,
                              form.recorded_department_id.data)
    return render_template('project/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def project_page(page=1):
    return index(page)


@bp.route('/detail/<project_id>', methods=['GET', 'POST'])
def detail(project_id=None):
    # basic
    project = service.find_by_id(project_id)

    if project.id is None and project_id is not None:
        return abort(404)

    form = ProjectForm(request.form, project)
    form.recorded_department_id.choices = department_service.find_all_for_select()
    form.client_company_id.choices = company_service.find_all_for_select()
    form.end_user_company_id.choices = company_service.find_all_for_select()
    form.assigned_members = project.assigned_members
    form.engineer_actual_results = project.get_engineer_actual_results()
    form.billings = project.get_billings()
    if form.validate_on_submit() and request.form["save"] == 'basic':
        project.project_name = form.project_name.data
        project.end_user_company_id = form.end_user_company_id.data
        project.client_company_id = form.client_company_id.data
        if project.start_date != form.start_date.data:
            project.is_start_date_change = True
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.recorded_department_id = form.recorded_department_id.data
        project.over_time_calculation_id = form.over_time_calculation_id.data
        project.contract_form = form.contract_form.data
        project.status = form.status.data
        project.billing_timing = form.billing_timing.data
        project.remarks = form.remarks.data

        service.save(project)
        flash('保存しました。')
        return redirect(url_for('.detail', project_id=project.id))
    current_app.logger.debug(form.errors)

    # estimation:
    if project.estimation_remarks is not None:
        estimation_remarks = project.estimation_remarks
    else:
        estimation_remarks = EstimationRemarks()

    estimation_remarks_form = EstimationRemarksForm(request.form, estimation_remarks)

    if estimation_remarks_form.validate_on_submit() and request.form["save"] == 'estimate':
        estimation_remarks.project_id = project.id
        estimation_remarks.scope = estimation_remarks_form.scope.data
        estimation_remarks.contents = estimation_remarks_form.contents.data
        estimation_remarks.deliverables = estimation_remarks_form.deliverables.data
        estimation_remarks.delivery_place = estimation_remarks_form.delivery_place.data
        estimation_remarks.inspection_date = estimation_remarks_form.inspection_date.data
        estimation_remarks.responsible_person = estimation_remarks_form.responsible_person.data
        estimation_remarks.quality_control = estimation_remarks_form.quality_control.data
        estimation_remarks.subcontractor = estimation_remarks_form.subcontractor.data

        estimation_remarks_service.save(estimation_remarks)
        flash('保存しました。')
        return redirect(url_for('.detail', project_id=project.id))
    current_app.logger.debug(estimation_remarks_form.errors)

    # order:
    if project.order_remarks is not None:
        order_remarks = project.order_remarks
    else:
        order_remarks = OrderRemarks()

    order_remarks_form = OrderRemarksForm(request.form, order_remarks)
    order_remarks_form.billing_company_id.choices = company_service.find_all_for_select()

    if order_remarks_form.validate_on_submit() and request.form["save"] == 'order':
        order_remarks.project_id = project.id
        order_remarks.order_no = order_remarks_form.order_no.data
        order_remarks.order_amount = order_remarks_form.order_amount.data
        order_remarks.contents = order_remarks_form.contents.data
        order_remarks.responsible_person = order_remarks_form.responsible_person.data
        order_remarks.subcontractor = order_remarks_form.subcontractor.data
        order_remarks.scope = order_remarks_form.scope.data
        order_remarks.work_place = order_remarks_form.work_place.data
        order_remarks.delivery_place = order_remarks_form.delivery_place.data
        order_remarks.deliverables = order_remarks_form.deliverables.data
        order_remarks.inspection_date = order_remarks_form.inspection_date.data
        order_remarks.payment_terms = order_remarks_form.payment_terms.data
        order_remarks.billing_company_id = order_remarks_form.billing_company_id.data
        order_remarks.remarks = order_remarks_form.remarks.data

        order_remarks_service.save(order_remarks)
        flash('保存しました。')
        return redirect(url_for('.detail', project_id=project.id))
    current_app.logger.debug(order_remarks_form.errors)

    return render_template('project/detail.html',
                           form=form,
                           estimation_remarks_form=estimation_remarks_form,
                           order_remarks_form=order_remarks_form,
                           project_attachments=project.get_project_attachments())


@bp.route('/create', methods=['GET', 'POST'])
def create():

    project = Project()

    form = ProjectCreateForm(request.form, project)
    if form.validate_on_submit():
        project.project_name = form.project_name.data

        service.save(project)
        flash('保存しました。')
        return redirect(url_for('.detail', project_id=project.id))
    current_app.logger.debug(form.errors)
    return render_template('project/create.html', form=form)


@bp.route('/copy/<project_id>', methods=['GET'])
def copy(project_id):
    project = service.clone(project_id)

    flash('コピーしました。')
    return redirect(url_for('.detail', project_id=project.id))


@bp.route('/delete/<project_id>', methods=['GET'])
def delete(project_id):
    project = service.find_by_id(project_id)
    if project.id is not None:
        service.destroy(project)
        flash('削除しました。')
    return redirect('/project')

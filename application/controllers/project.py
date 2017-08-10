from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.project_create_form import ProjectCreateForm
from application.controllers.form.project_search_form import ProjectSearchForm
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.message import Message
from application.domain.model.project import Project
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.page_session_service import PageSessionService
from application.service.project_detail_service import ProjectDetailService
from application.service.project_service import ProjectService
from application.service.search_session_service import SearchSessionService

bp = Blueprint('project', __name__, url_prefix='/project')
service = ProjectService()
project_detail_service = ProjectDetailService()
department_service = DepartmentService()
company_service = CompanyService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('project', request.args)
    search.save()
    page_session_service = PageSessionService(bp.name + '.index')
    page_session_service.save()

    form = ProjectSearchForm(search.get_dict())
    form.client_company_id.choices = company_service.find_for_multi_select_with_subtext_by_client_flag_id(
        [ClientFlag.client.value])
    form.end_user_company_id.choices = company_service.find_for_multi_select_with_subtext_by_client_flag_id(
        [ClientFlag.end_user.value])
    form.recorded_department_id.choices = department_service.find_all_for_multi_select()
    pagination = service.find(page,
                              form.project_name.data,
                              form.status.data,
                              form.end_user_company_id.data,
                              form.client_company_id.data,
                              form.recorded_department_id.data,                              
                              form.start_date.data,
                              form.end_date.data)
    return render_template('project/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def project_page(page=1):
    return index(page)


@bp.route('/create', methods=['GET', 'POST'])
def create(project_id=None):

    if project_id:
        project = service.find_by_id(project_id)
    else:
        project = Project()

    form = ProjectCreateForm(request.form, project)
    if form.validate_on_submit():
        if project_id:
            project = service.clone(project_id)
        project.project_name = form.project_name.data
        project.project_name_for_bp = form.project_name_for_bp.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        for detail in project.project_details:
            # BP注文番号を再発番したいので一旦ブランクで保存する
            detail.billing_start_day = None
            detail.billing_end_day = None
            # 顧客注文書No（BPごと）はブランクにする
            detail.client_order_no_for_bp = None

        service.save(project)

        # BP注文番号を再発番するため、開始日、終了日を設定する
        for detail in project.project_details:
            detail.billing_start_day = project.start_date
            detail.billing_end_day = project.end_date
            project_detail_service.save(detail)

        flash(Message.saved.value)
        return redirect(url_for('project_contract.index', project_id=project.id))
    current_app.logger.debug(form.errors)
    if form.errors:
        flash(Message.saving_failed.value, 'error')
    return render_template('project/create.html', form=form)


@bp.route('/copy/<project_id>', methods=['GET', 'POST'])
def copy(project_id):
    return create(project_id)


@bp.route('/delete/<project_id>', methods=['GET'])
def delete(project_id):
    project = service.find_by_id(project_id)
    if project.id is not None:
        service.destroy(project)
        flash(Message.deleted.value)
    return redirect('/project')

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.project_create_form import ProjectCreateForm
from application.controllers.form.project_search_form import ProjectSearchForm
from application.domain.model.project import Project
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.project_service import ProjectService

bp = Blueprint('project', __name__, url_prefix='/project')
service = ProjectService()
department_service = DepartmentService()
company_service = CompanyService()


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


@bp.route('/create', methods=['GET', 'POST'])
def create():

    project = Project()

    form = ProjectCreateForm(request.form, project)
    if form.validate_on_submit():
        project.project_name = form.project_name.data

        service.save(project)
        flash('保存しました。')
        return redirect(url_for('contract.index', project_id=project.id))
    current_app.logger.debug(form.errors)
    return render_template('project/create.html', form=form)


@bp.route('/copy/<project_id>', methods=['GET'])
def copy(project_id):
    project = service.clone(project_id)

    flash('コピーしました。')
    return redirect(url_for('contract.index', project_id=project.id))


@bp.route('/delete/<project_id>', methods=['GET'])
def delete(project_id):
    project = service.find_by_id(project_id)
    if project.id is not None:
        service.destroy(project)
        flash('削除しました。')
    return redirect('/project')

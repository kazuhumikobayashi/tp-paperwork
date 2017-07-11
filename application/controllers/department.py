from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.department_form import DepartmentForm
from application.controllers.form.department_search_form import DepartmentSearchForm
from application.service.department_service import DepartmentService
from application.service.search_session_service import SearchSessionService

bp = Blueprint('department', __name__, url_prefix='/department')
service = DepartmentService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('department', request.args)
    search.save()
    form = DepartmentSearchForm(search.get_dict())
    pagination = service.find(page, form.group_name.data, form.department_name.data)
    return render_template('master/department/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def department_page(page=1):
    return index(page)


@bp.route('/detail/<department_id>', methods=['GET', 'POST'])
def detail(department_id=None):
    department = service.find_by_id(department_id)

    if department.id is None and department_id is not None:
        return abort(404)
    form = DepartmentForm(request.form, department)

    if form.validate_on_submit():
        department.group_name = form.group_name.data
        department.department_name = form.department_name.data

        service.save(department)
        flash('保存しました。')
        return redirect(url_for('.detail', department_id=department.id))
    current_app.logger.debug(form.errors)
    return render_template('master/department/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<department_id>', methods=['GET'])
def delete(department_id):
    department = service.find_by_id(department_id)
    if department.id is not None:
        service.destroy(department)
        flash('削除しました。')
    return redirect('/department')

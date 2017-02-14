from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.department_form import DepartmentForm
from application.service.department_service import DepartmentService

bp = Blueprint('department', __name__, url_prefix='/department')
service = DepartmentService()


@bp.route('/', methods=['GET', 'POST'])
def index(page=1):
    department_name = request.args.get('department_name','')
    department_code = request.args.get('department_code','')
    pagination = service.find(page, department_name, department_code)
    return render_template('department/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET', 'POST'])
def department_page(page=1):
    return index(page)


@bp.route('/detail/<department_id>', methods=['GET', 'POST'])
def detail(department_id=None):
    department = service.find_by_id(department_id)

    if department is None and department_id is not None:
        return abort(404)
    form = DepartmentForm(request.form, department)

    if form.validate_on_submit():
        department.department_code = form.department_code.data
        department.department_name = form.department_name.data

        service.save(department)
        flash('保存しました。')
        return redirect(url_for('.detail', department_id=department.id))
    return render_template('department/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<department_id>', methods=['GET'])
def delete(department_id):
    department = service.find_by_id(department_id)
    if department is not None:
        service.destroy(department)
        flash('削除しました。')
    return redirect('/department')

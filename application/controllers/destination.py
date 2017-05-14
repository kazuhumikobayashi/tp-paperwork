from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.destination_form import DestinationForm
from application.controllers.form.destination_search_form import DestinationSearchForm
from application.service.company_service import CompanyService
from application.service.destination_service import DestinationService

bp = Blueprint('destination', __name__, url_prefix='/destination')
service = DestinationService()
company_service = CompanyService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = DestinationSearchForm(request.values)
    form.company_id.choices = company_service.find_all_for_multi_select()
    pagination = service.find(page, form.company_id.data, form.destination_name.data, form.destination_department.data)
    return render_template('destination/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def destination_page(page=1):
    return index(page)


@bp.route('/detail/<destination_id>', methods=['GET', 'POST'])
def detail(destination_id=None):
    destination = service.find_by_id(destination_id)

    if destination.id is None and destination_id is not None:
        return abort(404)
    form = DestinationForm(request.form, destination)
    form.company_id.choices = company_service.find_all_for_select()

    if form.validate_on_submit():
        destination.company_id = form.company_id.data
        destination.destination_name = form.destination_name.data
        destination.destination_department = form.destination_department.data

        service.save(destination)
        flash('保存しました。')
        return redirect(url_for('.detail', destination_id=destination.id))
    current_app.logger.debug(form.errors)
    return render_template('destination/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<destination_id>', methods=['GET'])
def delete(destination_id):
    destination = service.find_by_id(destination_id)
    if destination.id is not None:
        service.destroy(destination)
        flash('削除しました。')
    return redirect('/destination')

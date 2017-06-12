from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.project_month_form import ProjectMonthForm
from application.service.project_billing_service import ProjectBillingService
from application.service.project_month_service import ProjectMonthService
from application.service.project_service import ProjectService

bp = Blueprint('project_billing', __name__, url_prefix='/project_billing')
service = ProjectMonthService()
project_service = ProjectService()
billing_service = ProjectBillingService()


@bp.route('/<project_id>', methods=['GET', 'POST'])
def index(project_id=None):
    project = project_service.find_by_id(project_id)

    if project.id is None and project_id is not None:
        return abort(404)

    return render_template('project_billing/index.html',
                           project=project)


@bp.route('/detail/<project_month_id>', methods=['GET', 'POST'])
def detail(project_month_id=None):
    project_month = service.find_by_id(project_month_id)

    if project_month.id is None and project_month_id is not None:
        return abort(404)

    form = ProjectMonthForm(request.form, project_month)
    billings = billing_service.find_billings_at_a_month(project_month.project.id, project_month.project_month)

    if form.validate_on_submit():
        project_month.client_billing_no = form.client_billing_no.data
        project_month.billing_confirmation_money = form.billing_confirmation_money.data
        project_month.billing_transportation = form.billing_transportation.data
        project_month.deposit_date = form.deposit_date.data
        project_month.remarks = form.remarks.data

        service.save(project_month)
        flash('保存しました。')
        return redirect(url_for('.detail', project_month_id=project_month.id))

    current_app.logger.debug(form.errors)
    return render_template('project_billing/detail.html',
                           form=form,
                           billings=billings)

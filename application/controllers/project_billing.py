from flask import Blueprint, jsonify
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.project_billing_form import ProjectBillingForm
from application.controllers.form.project_month_form import ProjectMonthForm
from application.domain.model.immutables.input_flag import InputFlag
from application.service.project_billing_service import ProjectBillingService
from application.service.project_month_service import ProjectMonthService
from application.service.project_service import ProjectService

bp = Blueprint('project_billing', __name__, url_prefix='/project/billing')
project_service = ProjectService()
project_billing_service = ProjectBillingService()
project_month_service = ProjectMonthService()


@bp.route('/<project_id>', methods=['GET', 'POST'])
def index(project_id=None):
    project = project_service.find_by_id(project_id)

    if project.id is None and project_id is not None:
        return abort(404)

    return render_template('project/billing/index.html',
                           project=project)


@bp.route('/month/<project_month_id>', methods=['GET', 'POST'])
def month(project_month_id=None):
    project_month = project_month_service.find_by_id(project_month_id)

    if project_month.id is None and project_month_id is not None:
        return abort(404)

    form = ProjectMonthForm(request.form, project_month)
    billings = project_billing_service.find_billings_at_a_month(project_month.project.id, project_month.project_month)

    if form.validate_on_submit():
        project_month.client_billing_no = form.client_billing_no.data
        project_month.billing_confirmation_money = form.billing_confirmation_money.data
        project_month.billing_transportation = form.billing_transportation.data
        project_month.deposit_date = form.deposit_date.data
        project_month.remarks = form.remarks.data

        project_month_service.save(project_month)
        flash('保存しました。')
        return redirect(url_for('.month', project_month_id=project_month.id))

    current_app.logger.debug(form.errors)
    return render_template('project/billing/month.html',
                           form=form,
                           billings=billings)


@bp.route('/detail/<billing_id>', methods=['GET', 'POST'])
def detail(billing_id=None):
    billing = project_billing_service.find_by_id(billing_id)

    if billing.id is None and billing_id is not None:
        return abort(404)

    form = ProjectBillingForm(request.form, billing)

    project_month = project_month_service.find_project_month_at_a_month(
        billing.project_detail.project.id, billing.billing_month)

    if form.validate_on_submit():
        billing.billing_month = project_month.project_month
        billing.billing_content = form.billing_content.data
        billing.billing_amount = form.billing_amount.data
        billing.billing_confirmation_money = form.billing_confirmation_money.data
        billing.billing_transportation = form.billing_transportation.data
        billing.remarks = form.remarks.data

        project_billing_service.save(billing)
        flash('保存しました。')
        return redirect(url_for('.detail', billing_id=billing.id))

    current_app.logger.debug(form.errors)
    return render_template('project/billing/detail.html',
                           form=form,
                           project_month=project_month)


@bp.route('/delete/<billing_id>', methods=['GET'])
def delete(billing_id):
    billing = project_billing_service.find_by_id(billing_id)
    if billing.id is not None:
        project_month = project_month_service.find_project_month_at_a_month(billing.project_detail.project.id,
                                                                            billing.billing_month)
        project_billing_service.destroy(billing)
        flash('削除しました。')
        return redirect('/project/billing/detail/' + str(project_month.id))
    else:
        return redirect('/project/')


@bp.route('/save_flag', methods=['POST'])
def save_flag():
    if request.is_xhr:
        month_id = request.form["month_id"]
        input_flag = InputFlag.parse(request.form["input_flag"])

        project_month = project_month_service.find_by_id(month_id)
        project_month.billing_input_flag = input_flag

        project_month_service.save(project_month)
        return jsonify(result='success')

    return abort(404)

from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.billing_form import BillingForm
from application.service.project_billing_service import ProjectBillingService
from application.service.project_month_service import ProjectMonthService

bp = Blueprint('billing', __name__, url_prefix='/billing')
service = ProjectBillingService()
project_month_service = ProjectMonthService()


@bp.route('/<billing_id>', methods=['GET', 'POST'])
def detail(billing_id=None):
    billing = service.find_by_id(billing_id)

    if billing.id is None and billing_id is not None:
        return abort(404)

    form = BillingForm(request.form, billing)

    project_month = project_month_service.find_project_month_at_a_month(
        billing.project_detail.project.id, billing.billing_month)

    if form.validate_on_submit():
        billing.billing_month = project_month.project_month
        billing.billing_content = form.billing_content.data
        billing.billing_amount = form.billing_amount.data
        billing.billing_confirmation_money = form.billing_confirmation_money.data
        billing.billing_transportation = form.billing_transportation.data
        billing.remarks = form.remarks.data

        service.save(billing)
        flash('保存しました。')
        return redirect(url_for('.detail', billing_id=billing.id))

    current_app.logger.debug(form.errors)
    return render_template('billing/detail.html',
                           form=form,
                           project_month=project_month)


@bp.route('/delete/<billing_id>', methods=['GET'])
def delete(billing_id):
    billing = service.find_by_id(billing_id)
    if billing.id is not None:
        project_month = project_month_service.find_project_month_at_a_month(billing.project_detail.project.id,
                                                                            billing.billing_month)
        service.destroy(billing)
        flash('削除しました。')
        return redirect('/project_billing/detail/' + str(project_month.id))
    else:
        return redirect('/project/')

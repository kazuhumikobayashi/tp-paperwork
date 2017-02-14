from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.billing_form import BillingForm
from application.service.engineer_service import EngineerService
from application.service.billing_service import BillingService

bp = Blueprint('billing', __name__, url_prefix='/billing')
service = BillingService()
engineer_service = EngineerService()


@bp.route('/detail/<billing_id>', methods=['GET', 'POST'])
def detail(billing_id=None):
    billing = service.find_by_id(billing_id)
    if billing_id is None:
        billing.project_id = request.args.get('project_id', '')

    if billing is None and billing_id is not None:
        return abort(404)
    form = BillingForm(request.form, billing)

    if form.validate_on_submit():
        billing.project_id = form.project_id.data
        billing.billing_month = form.billing_month.data
        billing.billing_amount = form.billing_amount.data
        billing.billing_adjustment_amount = form.billing_adjustment_amount.data
        billing.tax = form.tax.data
        billing.carfare = form.carfare.data
        billing.scheduled_billing_date = form.scheduled_billing_date.data
        billing.billing_date = form.billing_date.data
        billing.bill_output_date = form.bill_output_date.data
        billing.scheduled_payment_date = form.scheduled_payment_date.data
        billing.payment_date = form.payment_date.data
        billing.status = form.status.data
        billing.remarks = form.remarks.data

        service.save(billing)
        flash('保存しました。')
        return redirect(url_for('.detail', billing_id=billing.id))
    return render_template('billing/detail.html', form=form)


@bp.route('/delete/<billing_id>', methods=['GET'])
def delete(billing_id):
    billing = service.find_by_id(billing_id)
    if billing is not None:
        service.destroy(billing)
        flash('削除しました。')
    return redirect(url_for('project.detail', project_id=billing.project_id) +
                    '?month=' + billing.billing_month.strftime('%Y%m'))

from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template

from application.controllers.form.output_form import OutputForm
from application.domain.model.immutables.output_type import OutputType
from application.service.payment_list_service import PaymentListService
from application.service.report.payment_list_report import PaymentListReport

bp = Blueprint('output', __name__, url_prefix='/output')

payment_list_service = PaymentListService()


@bp.route('/', methods=['GET', 'POST'])
def detail():
    form = OutputForm(request.form)

    if form.validate_on_submit():
        if form.output_report.data == str(OutputType.payment_list):
            project_lists_by_department = payment_list_service.get_payment_lists_by_department(form.month.data)
            project_list_by_payment_date\
                = payment_list_service.get_payment_list_order_by_payment_date(form.month.data)
            payment_list_report = PaymentListReport(project_lists_by_department,
                                                    project_list_by_payment_date,
                                                    form.month.data)
            return payment_list_report.download()

    current_app.logger.debug(form.errors)
    return render_template('output/download.html', form=form)

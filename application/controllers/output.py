from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template

from application.controllers.form.output_form import OutputForm
from application.domain.model.immutables.output_type import OutputType
from application.service.payment_list_service import PaymentListService
from application.service.project_detail_service import ProjectDetailService
from application.service.project_month_service import ProjectMonthService
from application.service.report.billing_department_report import BillingDepartmentReport
from application.service.report.payment_list_report import PaymentListReport
from application.service.report.project_list import ProjectList

bp = Blueprint('output', __name__, url_prefix='/output')

payment_list_service = PaymentListService()
project_detail_service = ProjectDetailService()
project_month_service = ProjectMonthService()


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
        elif form.output_report.data == str(OutputType.project_list):
            project_details_bp = project_detail_service.get_project_list_bp(form.month.data)
            project_details_our_company = project_detail_service.get_project_list_our_company(form.month.data)
            project_list = ProjectList(project_details_bp, project_details_our_company, form.month.data)
            return project_list.download()
        elif form.output_report.data == str(OutputType.billing_list):
            project_months = project_month_service.get_billing_department_report(form.month.data)
            billing_department_report = BillingDepartmentReport(project_months, form.month.data)
            return billing_department_report.download()

    current_app.logger.debug(form.errors)
    return render_template('output/download.html', form=form)

from flask import Blueprint
from flask import render_template
from flask import request

from application.controllers.form.billing_search_form import BillingSearchForm
from application.domain.model.immutables.client_flag import ClientFlag
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.project_billing_service import ProjectBillingService
from application.service.project_month_service import ProjectMonthService

bp = Blueprint('search_billing', __name__, url_prefix='/search/billing')
service = ProjectBillingService()
project_month_service = ProjectMonthService()
company_service = CompanyService()
department_service = DepartmentService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = BillingSearchForm(request.values)
    form.client_company_id.choices = company_service.find_for_select_by_client_flag_id(
        [ClientFlag.client.value])
    form.end_user_company_id.choices = company_service.find_for_select_by_client_flag_id(
        [ClientFlag.end_user.value])
    form.recorded_department_id.choices = department_service.find_all_for_multi_select()
    pagination = project_month_service.find_by_billing(page,
                                                       form.project_name.data,
                                                       form.result_input_flag.data,
                                                       form.billing_input_flag.data,
                                                       form.deposit_input_flag.data,
                                                       form.end_user_company_id.data,  
                                                       form.client_company_id.data,
                                                       form.recorded_department_id.data,                            
                                                       form.deposit_date_from.data,
                                                       form.deposit_date_to.data)
    return render_template('search/billing.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def payment_page(page=1):
    return index(page)

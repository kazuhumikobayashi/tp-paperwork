from flask import Blueprint
from flask import render_template
from flask import request

from application.controllers.form.payment_search_form import PaymentSearchForm
from application.domain.model.immutables.client_flag import ClientFlag
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.project_result_service import ProjectResultService

bp = Blueprint('payment', __name__, url_prefix='/search/payment')
service = ProjectResultService()
department_service = DepartmentService()
company_service = CompanyService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = PaymentSearchForm(request.values)
    form.client_company_id.choices = company_service.find_for_select_by_client_flag_id(
        [ClientFlag.client.value])
    form.end_user_company_id.choices = company_service.find_for_select_by_client_flag_id(
        [ClientFlag.end_user.value])
    form.recorded_department_id.choices = department_service.find_all_for_multi_select()
    pagination = service.find_by_payment(page,
                                         form.project_name.data,
                                         form.input_flag.data,
                                         form.end_user_company_id.data,
                                         form.client_company_id.data,
                                         form.recorded_department_id.data,  
                                         form.engineer_name.data,                            
                                         form.payment_expected_date_from.data,
                                         form.payment_expected_date_to.data)
    return render_template('payment/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def payment_page(page=1):
    return index(page)

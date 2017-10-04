from flask import Blueprint, abort, jsonify
from flask import render_template
from flask import request

from application.controllers.form.search_billing_form import SearchBillingForm
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.input_flag import InputFlag
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.page_session_service import PageSessionService
from application.service.project_billing_service import ProjectBillingService
from application.service.project_month_service import ProjectMonthService
from application.service.search_session_service import SearchSessionService

bp = Blueprint('search_billing', __name__, url_prefix='/search/billing')
service = ProjectBillingService()
project_month_service = ProjectMonthService()
company_service = CompanyService()
department_service = DepartmentService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('search_billing', request.args)
    search.save()
    page_session_service = PageSessionService(bp.name + '.index')
    page_session_service.save()

    form = SearchBillingForm(search.get_dict())
    form.client_company_id.choices = company_service.find_for_multi_select_with_subtext_by_client_flag_id(
        [ClientFlag.client.value])
    form.end_user_company_id.choices = company_service.find_for_multi_select_with_subtext_by_client_flag_id(
        [ClientFlag.end_user.value])
    form.recorded_department_id.choices = department_service.find_all_for_multi_select()
    pagination = project_month_service.find_by_billing(page,
                                                       form.project_name.data,
                                                       form.estimation_no.data,
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


@bp.route('/save_flag', methods=['POST'])
def save_flag():
    if request.is_xhr:
        month_id = request.form["month_id"]
        input_flag = InputFlag.parse(request.form["input_flag"])

        project_month = project_month_service.find_by_id(month_id)
        project_month.deposit_input_flag = input_flag

        project_month_service.save(project_month)
        return jsonify(result='success')

    return abort(404)

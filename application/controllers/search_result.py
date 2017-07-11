from flask import Blueprint
from flask import render_template
from flask import request

from application.controllers.form.search_result_form import SearchResultForm
from application.domain.model.immutables.client_flag import ClientFlag
from application.service.company_service import CompanyService
from application.service.department_service import DepartmentService
from application.service.project_result_service import ProjectResultService
from application.service.search_session_service import SearchSessionService

bp = Blueprint('search_result', __name__, url_prefix='/search/result')
project_result_service = ProjectResultService()
company_service = CompanyService()
department_service = DepartmentService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('search_result', request.args)
    search.save()
    form = SearchResultForm(search.get_dict())
    form.client_company_id.choices = company_service.find_for_multi_select_by_client_flag_id(
        [ClientFlag.client.value])
    form.end_user_company_id.choices = company_service.find_for_multi_select_by_client_flag_id(
        [ClientFlag.end_user.value])
    form.recorded_department_id.choices = department_service.find_all_for_multi_select()
    pagination = project_result_service.find_by_result(page,
                                                       form.project_name.data,
                                                       form.result_input_flag.data,
                                                       form.end_user_company_id.data,
                                                       form.client_company_id.data,
                                                       form.recorded_department_id.data,                            
                                                       form.engineer_name.data,
                                                       form.result_month_from.data,
                                                       form.result_month_to.data)
    return render_template('search/result.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def payment_page(page=1):
    return index(page)

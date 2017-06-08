from flask import Blueprint
from flask import render_template

from application.service.project_detail_service import ProjectDetailService
from application.service.project_month_service import ProjectMonthService
from application.service.project_service import ProjectService

bp = Blueprint('dashboard', __name__)
project_service = ProjectService()
project_detail_service = ProjectDetailService()
project_month_service = ProjectMonthService()


@bp.route('/', methods=['GET'])
def index():
    incomplete_estimates = project_service.find_incomplete_estimates()
    incomplete_results = project_month_service.find_incomplete_results()
    incomplete_billings = project_month_service.find_incomplete_billings()
    incomplete_payments = project_detail_service.find_incomplete_payments()
    incomplete_deposits = project_month_service.find_incomplete_deposits()
    return render_template('dashboard/index.html',
                           incomplete_estimates=incomplete_estimates,
                           incomplete_results=incomplete_results,
                           incomplete_billings=incomplete_billings,
                           incomplete_payments=incomplete_payments,
                           incomplete_deposits=incomplete_deposits)

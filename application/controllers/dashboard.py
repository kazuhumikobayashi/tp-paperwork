from flask import Blueprint
from flask import render_template

from application.service.project_service import ProjectService

bp = Blueprint('dashboard', __name__)
project_service = ProjectService()


@bp.route('/', methods=['GET'])
def index():
    incomplete_estimates = project_service.find_incomplete_estimates()
    incomplete_billings = project_service.find_incomplete_billings()
    incomplete_payments = project_service.find_incomplete_payments()
    return render_template('dashboard/index.html',
                           incomplete_estimates=incomplete_estimates,
                           incomplete_billings=incomplete_billings,
                           incomplete_payments=incomplete_payments)

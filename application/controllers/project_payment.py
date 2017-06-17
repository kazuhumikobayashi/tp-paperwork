from flask import Blueprint, render_template

from application.service.project_month_service import ProjectMonthService
from application.service.project_service import ProjectService

bp = Blueprint('project_payment', __name__, url_prefix='/project/payment')
project_service = ProjectService()
project_month_service = ProjectMonthService()


@bp.route('/<project_id>', methods=['GET'])
def index(project_id):
    project = project_service.find_by_id(project_id)
    form_data = project_month_service.get_project_payment_form(project.id)

    return render_template('project/payment/index.html',
                           project=project,
                           form_data=form_data)

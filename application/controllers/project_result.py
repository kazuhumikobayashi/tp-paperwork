from flask import Blueprint, render_template

from application.service.project_month_service import ProjectMonthService
from application.service.project_service import ProjectService

bp = Blueprint('project_result', __name__, url_prefix='/project_result')
project_service = ProjectService()
project_month_service = ProjectMonthService()


@bp.route('/<project_id>', methods=['GET'])
def index(project_id):
    project = project_service.find_by_id(project_id)
    form_data = project_month_service.get_project_result_form(project.id)

    return render_template('project_result/index.html',
                           project=project,
                           form_data=form_data)

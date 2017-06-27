from flask import Blueprint, render_template, abort, request, flash, redirect, url_for, current_app, jsonify

from application.controllers.form.result_form import ResultForm, ProjectDetailInResultForm, EngineerHistoryInResultForm
from application.domain.model.immutables.input_flag import InputFlag
from application.service.engineer_history_service import EngineerHistoryService
from application.service.project_month_service import ProjectMonthService
from application.service.project_result_service import ProjectResultService
from application.service.project_service import ProjectService

bp = Blueprint('project_result', __name__, url_prefix='/project/result')
project_service = ProjectService()
project_month_service = ProjectMonthService()
project_result_service = ProjectResultService()
engineer_history_service = EngineerHistoryService()


@bp.route('/<project_id>', methods=['GET'])
def index(project_id):
    project = project_service.find_by_id(project_id)
    form_data = project_month_service.get_project_result_form(project.id)

    return render_template('project/result/index.html',
                           project=project,
                           form_data=form_data)


@bp.route('/detail/<result_id>', methods=['GET', 'POST'])
def detail(result_id=None):
    result = project_result_service.find_by_id(result_id)
    pre_page = request.args.get('pre_page', 'result')

    if result.id is None and result_id is not None:
        return abort(404)

    engineer_history = engineer_history_service.get_history_at_result_month(result.project_detail.engineer_id,
                                                                            result.result_month)

    form = ResultForm(request.form, result)
    project_detail_form = ProjectDetailInResultForm(obj=result.project_detail)
    engineer_history_form = EngineerHistoryInResultForm(obj=engineer_history)

    form.engineer_name.data = result.project_detail.engineer.engineer_name

    if form.validate_on_submit():
        result.work_time = form.work_time.data
        result.billing_transportation = form.billing_transportation.data
        result.billing_adjustments = form.billing_adjustments.data
        result.billing_confirmation_number = form.billing_confirmation_number.data
        result.billing_confirmation_money = form.billing_confirmation_money.data
        result.payment_transportation = form.payment_transportation.data
        result.payment_adjustments = form.payment_adjustments.data
        result.payment_confirmation_money = form.payment_confirmation_money.data
        result.remarks = form.remarks.data
        result.payment_expected_date = form.payment_expected_date.data

        project_result_service.save(result)
        flash('保存しました。')
        query_strings = '' if pre_page == 'result' else '?pre_page=' + pre_page
        return redirect(url_for('.detail', result_id=result.id) + query_strings)
    current_app.logger.debug(form.errors)
    return render_template('project/result/detail.html',
                           form=form,
                           project_detail_form=project_detail_form,
                           engineer_history_form=engineer_history_form,
                           pre_page=pre_page)

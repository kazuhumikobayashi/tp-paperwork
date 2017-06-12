from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.result_form import ResultForm, ProjectDetailInResultForm, EngineerHistoryInResultForm
from application.service.engineer_history_service import EngineerHistoryService
from application.service.project_result_service import ProjectResultService

bp = Blueprint('result', __name__, url_prefix='/result')
service = ProjectResultService()
engineer_history_service = EngineerHistoryService()


@bp.route('/<result_id>', methods=['GET', 'POST'])
def detail(result_id=None):
    result = service.find_by_id(result_id)

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

        service.save(result)
        flash('保存しました。')
        return redirect(url_for('.detail', result_id=result.id))
    current_app.logger.debug(form.errors)
    return render_template('result/detail.html',
                           form=form,
                           project_detail_form=project_detail_form,
                           engineer_history_form=engineer_history_form,
                           result=result)

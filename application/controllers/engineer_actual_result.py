from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.engineer_actual_result_form import EngineerActualResultForm
from application.service.engineer_service import EngineerService
from application.service.engineer_actual_result_service import EngineerActualResultService

bp = Blueprint('engineer_actual_result', __name__, url_prefix='/engineer_actual_result')
service = EngineerActualResultService()
engineer_service = EngineerService()


@bp.route('/detail/<engineer_actual_result_id>', methods=['GET', 'POST'])
def detail(engineer_actual_result_id=None):
    engineer_actual_result = service.find_by_id(engineer_actual_result_id)
    if engineer_actual_result_id is None:
        engineer_actual_result.project_id = request.args.get('project_id', '')
    current_app.logger.debug(engineer_actual_result)

    if engineer_actual_result.id is None and engineer_actual_result_id is not None:
        return abort(404)
    form = EngineerActualResultForm(request.form, engineer_actual_result)
    form.engineer_id.choices = engineer_service.find_all_for_select()

    if form.validate_on_submit():
        engineer_actual_result.project_id = form.project_id.data
        engineer_actual_result.fixed_flg = form.fixed_flg.data or '0'
        engineer_actual_result.seq_no = 1
        engineer_actual_result.engineer_id = form.engineer_id.data
        engineer_actual_result.working_hours = form.working_hours.data
        engineer_actual_result.adjustment_hours = form.adjustment_hours.data
        engineer_actual_result.billing_amount = form.billing_amount.data
        engineer_actual_result.billing_adjustment_amount = form.billing_adjustment_amount.data
        engineer_actual_result.payment_amount = form.payment_amount.data
        engineer_actual_result.payment_adjustment_amount = form.payment_adjustment_amount.data
        engineer_actual_result.carfare = form.carfare.data
        engineer_actual_result.remarks = form.remarks.data

        service.save(engineer_actual_result)
        flash('保存しました。')
        return redirect(url_for('.detail', engineer_actual_result_id=engineer_actual_result.id))
    current_app.logger.debug(form.errors)
    return render_template('engineer_actual_result/detail.html', form=form)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    return detail()


@bp.route('/delete/<engineer_actual_result_id>', methods=['GET'])
def delete(engineer_actual_result_id):
    engineer_actual_result = service.find_by_id(engineer_actual_result_id)

    if engineer_actual_result.id is None:
        return abort(404)
    else:
        service.destroy(engineer_actual_result)
        flash('削除しました。')
    return redirect(url_for('project.detail', project_id=engineer_actual_result.project_id) +
                    '?month=' + engineer_actual_result.result_month.strftime('%Y%m'))

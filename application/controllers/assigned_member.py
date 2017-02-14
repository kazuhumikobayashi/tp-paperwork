from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.assigned_member_form import AssignedMemberForm
from application.service.engineer_service import EngineerService
from application.service.assigned_member_service import AssignedMemberService

bp = Blueprint('assigned_member', __name__, url_prefix='/assigned_member')
service = AssignedMemberService()
engineer_service = EngineerService()


@bp.route('/detail/<assigned_member_id>', methods=['GET', 'POST'])
def detail(assigned_member_id=None):
    assigned_member = service.find_by_id(assigned_member_id)
    if assigned_member_id is None:
        assigned_member.project_id = request.args.get('project_id', '')
    current_app.logger.debug(str(assigned_member))

    if assigned_member is None and assigned_member_id is not None:
        return abort(404)
    form = AssignedMemberForm(request.form, assigned_member)
    form.engineer_id.choices = engineer_service.find_all_for_select()

    if form.validate_on_submit():
        assigned_member.project_id = form.project_id.data
        assigned_member.seq_no = 1
        assigned_member.engineer_id = form.engineer_id.data
        assigned_member.sales_unit_price = form.sales_unit_price.data
        assigned_member.payment_unit_price = form.payment_unit_price.data
        assigned_member.start_date = form.start_date.data
        assigned_member.end_date = form.end_date.data

        service.save(assigned_member)
        flash('保存しました。')
        return redirect(url_for('.detail', assigned_member_id=assigned_member.id))
    return render_template('assigned_member/detail.html', form=form)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    return detail()


@bp.route('/delete/<assigned_member_id>', methods=['GET'])
def delete(assigned_member_id):
    assigned_member = service.find_by_id(assigned_member_id)
    if assigned_member is not None:
        service.destroy(assigned_member)
        flash('削除しました。')
    return redirect(url_for('project.detail', project_id=assigned_member.project_id))

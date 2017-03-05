from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.engineer_form import EngineerForm
from application.controllers.form.engineer_search_form import EngineerSearchForm
from application.domain.model.engineer_skill import EngineerSkill
from application.service.company_service import CompanyService
from application.service.engineer_service import EngineerService
from application.service.skill_service import SkillService

bp = Blueprint('engineer', __name__, url_prefix='/engineer')
service = EngineerService()
company_service = CompanyService()
skill_service = SkillService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = EngineerSearchForm(request.values)
    form.company_id.choices = company_service.find_all_for_multi_select()
    form.skill_id.choices = skill_service.find_all_for_multi_select()

    pagination = service.find(page, form.engineer_name.data, form.company_id.data, form.skill_id.data)
    return render_template('engineer/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def engineer_page(page=1):
    return index(page)


@bp.route('/detail/<engineer_id>', methods=['GET', 'POST'])
def detail(engineer_id=None):
    engineer = service.find_by_id(engineer_id)

    if engineer.id is None and engineer_id is not None:
        return abort(404)
    engineer.skill = [h.skill_id for h in engineer.engineer_skills]
    form = EngineerForm(request.form, engineer)
    form.company_id.choices = company_service.find_all_for_select()
    form.skill.choices = skill_service.find_all_for_multi_select()

    if form.validate_on_submit():
        engineer.start_date = form.start_date.data
        engineer.end_date = form.end_date.data
        engineer.engineer_name = form.engineer_name.data
        engineer.engineer_name_kana = form.engineer_name_kana.data
        engineer.company_id = form.company_id.data
        engineer.remarks = form.remarks.data
        skills = []
        for skill_id in form.skill.data:
            skills.extend([EngineerSkill(engineer.id, skill_id)])
        engineer.engineer_skills = skills

        service.save(engineer)
        flash('保存しました。')
        return redirect(url_for('.detail', engineer_id=engineer.id))
    current_app.logger.debug(form.errors)
    return render_template('engineer/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<engineer_id>', methods=['GET'])
def delete(engineer_id):
    engineer = service.find_by_id(engineer_id)
    if engineer.id is not None:
        service.destroy(engineer)
        flash('削除しました。')
    return redirect('/engineer')

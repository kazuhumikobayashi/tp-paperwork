from flask import Blueprint, current_app
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.skill_form import SkillForm
from application.controllers.form.skill_search_form import SkillSearchForm
from application.domain.model.immutables.message import Message
from application.service.search_session_service import SearchSessionService
from application.service.skill_service import SkillService

bp = Blueprint('skill', __name__, url_prefix='/skill')
service = SkillService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('skill', request.args)
    search.save()
    form = SkillSearchForm(search.get_dict())
    pagination = service.find(page, form.skill_name.data)
    return render_template('master/skill/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def skill_page(page=1):
    return index(page)


@bp.route('/detail/<skill_id>', methods=['GET', 'POST'])
def detail(skill_id=None):
    skill = service.find_by_id(skill_id)

    if skill.id is None and skill_id is not None:
        return abort(404)
    form = SkillForm(request.form, obj=skill)

    if form.validate_on_submit():
        skill.skill_name = form.skill_name.data

        service.save(skill)
        flash(Message.saved.value)
        return redirect(url_for('.detail', skill_id=skill.id))
    current_app.logger.debug(form.errors)
    if form.errors:
        flash(Message.saving_failed.value, 'error')
    return render_template('master/skill/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<skill_id>', methods=['GET'])
def delete(skill_id):
    skill = service.find_by_id(skill_id)
    if skill.id is not None:
        service.destroy(skill)
        flash(Message.deleted.value)
    return redirect('/skill')

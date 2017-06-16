from flask import Blueprint
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.skill_form import SkillForm
from application.service.skill_service import SkillService

bp = Blueprint('skill', __name__, url_prefix='/skill')
service = SkillService()


@bp.route('/', methods=['GET'])
def index(page=1):
    skill_name = request.args.get('skill_name', '')
    pagination = service.find(page, skill_name)
    return render_template('master/skill/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET'])
def skill_page(page=1):
    return index(page)


@bp.route('/detail/<skill_id>', methods=['GET', 'POST'])
def detail(skill_id=None):
    skill = service.find_by_id(skill_id)

    if skill.id is None and skill_id is not None:
        return abort(404)
    form = SkillForm(request.form, skill)

    if form.validate_on_submit():
        skill.skill_name = form.skill_name.data

        service.save(skill)
        flash('保存しました。')
        return redirect(url_for('.detail', skill_id=skill.id))
    return render_template('master/skill/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<skill_id>', methods=['GET'])
def delete(skill_id):
    skill = service.find_by_id(skill_id)
    if skill.id is not None:
        service.destroy(skill)
        flash('削除しました。')
    return redirect('/skill')

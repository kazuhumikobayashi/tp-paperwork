from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.project_attachment_form import ProjectAttachmentForm, FileForm
from application.domain.model.immutables.project_attachment_type import ProjectAttachmentType
from application.service.attachment_service import AttachmentService
from application.service.project_attachment_service import ProjectAttachmentService

bp = Blueprint('project_attachment', __name__, url_prefix='/project_attachment')
service = ProjectAttachmentService()
attachment_service = AttachmentService()


@bp.route('/detail/<project_attachment_id>', methods=['GET', 'POST'])
def detail(project_attachment_id=None):
    project_attachment = service.find_by_id(project_attachment_id)

    if project_attachment.id is None and project_attachment_id is not None:
        return abort(404)
    form = ProjectAttachmentForm(request.form, project_attachment)
    file_form = FileForm()

    if project_attachment.id is None:
        form.project_id.data = request.args.get('project_id', '')
    else:
        form.filename.data = project_attachment.attachment.filename
        file_form.attachment_id.data = project_attachment.attachment_id

    if form.validate_on_submit() and file_form.validate_on_submit():

        file = file_form.upload.data
        attachment = attachment_service.save(file)

        project_attachment.project_id = form.project_id.data
        project_attachment.attachment_id = attachment.id or file_form.attachment_id.data
        project_attachment.type = ProjectAttachmentType.parse(form.type.data)
        project_attachment.remarks = form.remarks.data
        service.save(project_attachment)
        flash('保存しました。')
        return redirect(url_for('.detail', project_attachment_id=project_attachment.id))
    current_app.logger.debug(form.errors)
    current_app.logger.debug(file_form.errors)
    return render_template('project_attachment/detail.html', form=form, file_form=file_form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<project_attachment_id>', methods=['GET'])
def delete(project_attachment_id):
    project_attachment = service.find_by_id(project_attachment_id)

    if project_attachment.id is None:
        return abort(404)
    else:
        # storageのファイルを削除
        service.destroy(project_attachment)
        attachment = attachment_service.find_by_id(project_attachment.attachment_id)
        attachment_service.destroy(attachment)
        flash('削除しました。')
    return redirect(url_for('project.detail', project_id=project_attachment.project_id))

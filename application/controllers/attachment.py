from flask import Blueprint

from application.service.attachment_service import AttachmentService

bp = Blueprint('attachment', __name__, url_prefix='/attachment')
service = AttachmentService()


@bp.route('/download/<attachment_id>', methods=['GET', 'POST'])
def download(attachment_id=None):
    return service.download(attachment_id)

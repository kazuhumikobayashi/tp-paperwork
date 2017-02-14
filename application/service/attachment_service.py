from urllib import parse

from flask import current_app
from flask import make_response

from application.domain.repository.attachment_repository import AttachmentRepository
from application.service.google import storage


class AttachmentService(object):
    repository = AttachmentRepository()

    def find_by_id(self, attachment_id):
        return self.repository.find_by_id(attachment_id)

    def download(self, attachment_id):
        attachment = self.repository.find_by_id(attachment_id)
        blob = storage.download_file(attachment.storage_filename)
        response = make_response()

        dispostion = "attachment; filename*=UTF-8''"
        # 日本語をUrlエンコード
        dispostion += parse.quote(attachment.filename)
        if blob:
            response.data = blob.download_as_string()
        response.headers['Content-Disposition'] = dispostion
        response.headers['Content-Type'] = attachment.content_type

        return response

    def save(self, file):
        attachment = self.repository.create()
        if file is not None:
            blob = file.read()
            filename = file.filename
            content_type = file.content_type
            storage_filename = storage.upload_file(
                blob,
                filename,
                content_type
            )
            current_app.logger.debug(
                "Uploaded file %s as %s.", filename, storage_filename)

            attachment.filename = filename
            attachment.storage_filename = storage_filename
            attachment.size = len(blob)
            attachment.content_type = content_type

            self.repository.save(attachment)
        return attachment

    def destroy(self, attachment):
        storage.delete_file(attachment.storage_filename)
        self.repository.destroy(attachment)

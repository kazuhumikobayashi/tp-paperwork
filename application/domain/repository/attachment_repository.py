from application.domain.model.attachment import Attachment
from application.domain.repository.base_repository import BaseRepository


class AttachmentRepository(BaseRepository):

    model = Attachment

    def create(self):
        return Attachment()

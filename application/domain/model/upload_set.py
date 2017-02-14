class UploadSet(object):
    def __init__(self, name='files', extensions=None):
        self.name = name
        self.extensions = extensions

    def file_allowed(self, storage, basename):
        if not self.extensions:
            return True

        ext = basename.rsplit('.', 1)[-1]
        return ext in self.extensions

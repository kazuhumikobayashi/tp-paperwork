class Search(object):

    def __init__(self, page, request_args):
        self.page = page
        self.request_args = dict(request_args)

    def __repr__(self):
        return "<Search:" + \
                "'request_args='{}".format(self.request_args) + \
                "', page='{}".format(self.page) + \
                "'>"

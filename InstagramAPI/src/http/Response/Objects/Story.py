from InstagramAPI.src.http.Response.Response import Response


class Story(Response):
    def __init__(self):
        self.pk = None
        self.counts = None
        self.args = None
        self.__dict__["type"] = None

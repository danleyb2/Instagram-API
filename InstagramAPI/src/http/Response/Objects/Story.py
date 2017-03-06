from InstagramAPI.src.http.Response.Response import Response


class Story(Response):
    def __init__(self):
        self._types = {}

        self._types["pk"] = str
        self.pk = None
        self.counts = None
        self.args = None
        self.type = None

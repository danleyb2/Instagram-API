from InstagramAPI.src.http.Response.Response import Response


class Link(Response):
    def __init__(self):
        self._types = {}

        self.start = None
        self.end = None
        self._types["id"] = str
        self.id = None
        self.type = None

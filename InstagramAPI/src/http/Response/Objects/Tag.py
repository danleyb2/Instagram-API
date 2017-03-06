from InstagramAPI.src.http.Response.Response import Response


class Tag(Response):
    def __init__(self):
        self._types = {}

        self.media_count = None
        self.name = None
        self._types["id"] = str
        self.id = None

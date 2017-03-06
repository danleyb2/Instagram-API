from InstagramAPI.src.http.Response.Response import Response


class TagRelatedResponse(Response):
    def __init__(self):
        self._types = {}

        self.related = None

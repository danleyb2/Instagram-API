from InstagramAPI.src.http.Response.Response import Response


class _Message(Response):
    def __init__(self):
        self._types = {}

        self.key = None
        self.time = None

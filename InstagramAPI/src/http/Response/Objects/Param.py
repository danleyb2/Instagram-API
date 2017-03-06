from InstagramAPI.src.http.Response.Response import Response


class Param(Response):
    def __init__(self):
        self._types = {}

        self.name = None
        self.value = None

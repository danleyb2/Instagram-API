from InstagramAPI.src.http.Response.Response import Response


class MegaphoneLogResponse(Response):
    def __init__(self):
        self._types = {}

        self.success = None

from InstagramAPI.src.http.Response.Response import Response


class TagInfoResponse(Response):
    def __init__(self):
        self._types = {}

        self.profile = None
        self.media_count = None

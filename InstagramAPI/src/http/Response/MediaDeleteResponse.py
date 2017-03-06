from InstagramAPI.src.http.Response.Response import Response


class MediaDeleteResponse(Response):
    def __init__(self):
        self._types = {}

        self.did_delete = None

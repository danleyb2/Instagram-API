from InstagramAPI.src.http.Response.Response import Response


class VideoVersions(Response):
    def __init__(self):
        self._types = {}

        self.url = None
        self.type = None
        self.width = None
        self.height = None

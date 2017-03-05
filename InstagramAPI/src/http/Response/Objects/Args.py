from InstagramAPI.src.http.Response.Response import Response


class Args(Response):
    def __init__(self):
        self._types = {}

        self.media = None
        self.links = None
        self.text = None
        self._types["profile_id"] = str
        self.profile_id = None
        self.profile_image = None
        self.timestamp = None

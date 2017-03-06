from InstagramAPI.src.http.Response.Response import Response


class Hashtags(Response):
    def __init__(self):
        self._types = {}

        self.position = None
        self.hashtag = None

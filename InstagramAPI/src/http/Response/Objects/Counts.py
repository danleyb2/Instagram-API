from InstagramAPI.src.http.Response.Response import Response


class Counts(Response):
    def __init__(self):
        self._types = {}

        self.relationships = None
        self.requests = None
        self.photos_of_you = None

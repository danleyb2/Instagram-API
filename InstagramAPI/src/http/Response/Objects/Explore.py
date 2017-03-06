from InstagramAPI.src.http.Response.Response import Response


class Explore(Response):
    def __init__(self):
        self._types = {}

        self.explanation = None
        self._types["actor_id"] = str
        self.actor_id = None
        self.source_token = None

from InstagramAPI.src.http.Response.Response import Response


class Explore(Response):
    def __init__(self):
        self.explanation = None
        self.actor_id = None
        self.source_token = None

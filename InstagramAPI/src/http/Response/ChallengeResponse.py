from InstagramAPI.src.http.Response.Response import Response


class ChallengeResponse(Response):
    def __init__(self):
        self._types = {}

        self.status = None

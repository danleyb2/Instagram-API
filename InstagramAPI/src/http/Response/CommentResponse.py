from InstagramAPI.src.http.Response.Response import Response


class CommentResponse(Response):
    def __init__(self):
        self._types = {}

        self.comment = None

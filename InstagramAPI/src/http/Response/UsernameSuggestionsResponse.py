from InstagramAPI.src.http.Response.Response import Response


class UsernameSuggestionsResponse(Response):
    def __init__(self):
        self._types = {}

        self.username_suggestions = None

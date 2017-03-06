from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Response import Response


class UsernameInfoResponse(Response):
    def __init__(self):
        self._types = {}

        self.megaphone = None
        self._types["user"] = User
        self.user = None

from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Response import Response


class Users(Response):
    def __init__(self):
        self._types = {}

        self.position = None
        self._types["user"] = User
        self.user = None

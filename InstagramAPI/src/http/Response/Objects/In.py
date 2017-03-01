from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.Position import Position
from InstagramAPI.src.http.Response.Objects.User import User


class In(Response):
    def __init__(self):
        self._types = {}
        self._types["position"] = Position
        self.position = None
        self._types["user"] = User
        self.user = None

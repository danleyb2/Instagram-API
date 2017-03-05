from InstagramAPI.src.http.Response.Response import Response
from .User import User


class Comment(Response):
    def __init__(self):
        self._types = {}

        self.status = None
        self._types["username_id"] = str
        self.username_id = None
        self.created_at_utc = None
        self.created_at = None
        self.bit_flags = None
        self._types["user"] = User
        self.user = None
        self._types["pk"] = str
        self.pk = None
        self.text = None

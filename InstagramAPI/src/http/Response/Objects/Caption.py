from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.User import User


class Caption(Response):
    def __init__(self):
        self._types = {}

        self.status = None
        self.user_id = None
        self.created_at_utc = None
        self.created_at = None
        self.bit_flags = None
        self._types["user"] = User
        self.user = None
        self.content_type = None
        self.text = None
        self.media_id = None
        self.pk = None
        self.type = None
        self.has_translation = None

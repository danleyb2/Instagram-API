from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Response import Response


class Reel(Response):
    def __init__(self):
        self._types = {}

        self._types["id"] = str
        self.id = None
        self._types["items"] = [Item]
        self.items = None
        self.user = None
        self.expiring_at = None
        self.seen = None
        self.can_reply = None

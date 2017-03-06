from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Response import Response


class EditMediaResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["media"] = Item
        self.media = None

from InstagramAPI.src.http.Response.Objects.SavedFeedItem import SavedFeedItem
from InstagramAPI.src.http.Response.Response import Response


class SavedFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["items"] = [SavedFeedItem]
        self.items = None

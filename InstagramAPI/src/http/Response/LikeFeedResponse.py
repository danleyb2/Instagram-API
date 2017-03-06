from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Response import Response


class LikeFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self.auto_load_more_enabled = None
        self._types["items"] = [Item]
        self.items = None
        self.more_available = None
        self.patches = None
        self.last_counted_at = None
        self.num_results = None

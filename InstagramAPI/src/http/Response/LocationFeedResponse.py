from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Response import Response


class LocationFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self.media_count = None
        self.num_results = None
        self.auto_load_more_enabled = None
        self._types["items"] = [Item]
        self.items = None
        self._types["ranked_items"] = [Item]
        self.ranked_items = None
        self.more_available = None
        self._types["next_max_id"] = str
        self.next_max_id = None

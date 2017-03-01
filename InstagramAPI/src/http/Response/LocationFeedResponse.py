from .Response import Response
from .Objects.Item import Item


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
        self.next_max_id = None

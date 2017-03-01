from .Response import Response
from .Objects.Item import Item


class PopularFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self.next_max_id = None
        self.more_available = None
        self.auto_load_more_enabled = None
        self._types["items"] = [Item]
        self.items = None
        self.num_results = None
        self.max_id = None

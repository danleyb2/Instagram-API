from .Objects.Item import Item
from .Response import Response


class UserFeedResponse(Response):
    def __init__(self):
        self._types = {}
        self.num_results = None
        self.auto_load_more_enabled = None
        self._types["items"] = [Item]
        self.items = None
        self.more_available = None
        self.next_max_id = None

from .Response import Response
from .Objects.Item import Item


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

from InstagramAPI.src.http.Response.Objects.FeedAysf import FeedAysf
from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Objects._Message import _Message
from InstagramAPI.src.http.Response.Response import Response


class TimelineFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self.num_results = None
        self.is_direct_v2_enabled = None
        self.auto_load_more_enabled = None
        self.more_available = None
        self._types["next_max_id"] = str
        self.next_max_id = None
        self._types["_messages"] = [_Message]
        self._messages = None
        self._types["feed_items"] = [Item]
        self.feed_items = None
        self._types["megaphone"] = FeedAysf
        self.megaphone = None

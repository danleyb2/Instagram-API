from .Response import Response


class TimelineFeedResponse(Response):
    def __init__(self):

        self.num_results = None
        self.is_direct_v2_enabled = None
        self.auto_load_more_enabled = None
        self.more_available = None
        self.next_max_id = None
        self._messages = None
        self.feed_items = None
        self.megaphone = None

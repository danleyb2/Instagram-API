from .Response import Response
from .Objects.Story import Story


class ActivityNewsResponse(Response):
    def __init__(self):
        self._types = {}
        self._types["new_stories"] = [Story]
        self.new_stories = None
        self._types["old_stories"] = [Story]
        self.old_stories = None
        self.continuation = None
        self.friend_request_stories = None
        self.counts = None
        self.subscription = None
        self.continuation_token = None

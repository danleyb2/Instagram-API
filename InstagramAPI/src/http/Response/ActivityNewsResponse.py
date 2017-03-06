from InstagramAPI.src.http.Response.Objects.Story import Story
from InstagramAPI.src.http.Response.Response import Response


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
        self._types["subscription"] = mixed
        self.subscription = None
        self.continuation_token = None

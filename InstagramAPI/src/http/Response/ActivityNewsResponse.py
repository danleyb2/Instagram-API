from .Response import Response


class ActivityNewsResponse(Response):
    def __init__(self):
        self.new_stories = None
        self.old_stories = None
        self.continuation = None
        self.friend_request_stories = None
        self.counts = None
        self.subscription = None
        self.continuation_token = None

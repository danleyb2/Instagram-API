from InstagramAPI.src.http.Response.Objects.Thread import Thread
from InstagramAPI.src.http.Response.Response import Response


class Inbox(Response):
    def __init__(self):
        self._types = {}

        self.unseen_count = None
        self.has_older = None
        self.unseen_count_ts = None
        self._types["threads"] = [Thread]
        self.threads = None

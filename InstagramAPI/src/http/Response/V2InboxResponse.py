from InstagramAPI.src.http.Response.Objects.Inbox import Inbox
from InstagramAPI.src.http.Response.Response import Response


class V2InboxResponse(Response):
    def __init__(self):
        self._types = {}

        self.pending_requests_total = None
        self._types["seq_id"] = str
        self.seq_id = None
        self.pending_requests_users = None
        self._types["inbox"] = Inbox
        self.inbox = None
        self.subscription = None

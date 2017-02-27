from .Response import Response
from .Objects.Inbox import Inbox


class V2InboxResponse(Response):
    def __init__(self):
        self._types = {}

        self.pending_requests_total = None
        self.seq_id = None
        self.pending_requests_users = None
        self._types["inbox"] = Inbox
        self.inbox = None
        self.subscription = None

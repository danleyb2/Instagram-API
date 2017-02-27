from .Response import Response


class V2InboxResponse(Response):
    def __init__(self):
        self.pending_requests_total = None
        self.seq_id = None
        self.pending_requests_users = None
        self.inbox = None
        self.subscription = None

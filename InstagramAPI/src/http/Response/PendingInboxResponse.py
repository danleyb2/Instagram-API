from InstagramAPI.src.http.Response.Response import Response


class PendingInboxResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["seq_id"] = str
        self.seq_id = None
        self.pending_requests_total = None
        self.inbox = None

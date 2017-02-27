from InstagramAPI.src.http.Response.Objects.Inbox import Inbox
from .Response import Response


class PendingInboxResponse(Response):
    def __init__(self, response):
        self.seq_id = None
        self.pending_requests_total = None
        self.inbox = None

        if self.STATUS_OK == response['status']:
            self.seq_id = response['seq_id']
            self.pending_requests_total = response['pending_requests_total']
            self.inbox = Inbox(response['inbox'])
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getSeqId(self):
        return self.seq_id

    def getPendingRequestsTotal(self):
        return self.pending_requests_total

    def getInbox(self):
        return self.inbox

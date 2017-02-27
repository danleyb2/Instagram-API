from InstagramAPI.src.http.Response.Objects.Inbox import Inbox
from .Response import Response


class V2InboxResponse(Response):
    def __init__(self, response):
        self.pending_requests_total = None
        self.seq_id = None
        self.pending_requests_users = None
        self.inbox = None
        self.subscription = None

        if self.STATUS_OK == response['status']:
            self.pending_requests_total = response['pending_requests_total']
            self.seq_id = response['seq_id']
            self.pending_requests_users = response['pending_requests_users']
            self.inbox = Inbox(response['inbox'])
            self.subscription = response['subscription']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getPendingRequestsTotal(self):
        return self.pending_requests_total

    def getSeqId(self):
        return self.seq_id

    def getPendingRequestsUsers(self):
        return self.pending_requests_users

    def getInbox(self):
        return self.inbox

    def getSubscription(self):
        return self.subscription

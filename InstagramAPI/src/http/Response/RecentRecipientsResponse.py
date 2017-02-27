from .Response import Response


class RecentRecipientsResponse(Response):
    def __init__(self):
        self.expiration_interval = None
        self.recent_recipients = None

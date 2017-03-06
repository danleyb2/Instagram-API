from InstagramAPI.src.http.Response.Response import Response


class RecentRecipientsResponse(Response):
    def __init__(self):
        self._types = {}

        self.expiration_interval = None
        self.recent_recipients = None

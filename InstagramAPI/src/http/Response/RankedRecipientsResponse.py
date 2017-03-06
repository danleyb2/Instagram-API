from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Response import Response


class RankedRecipientsResponse(Response):
    def __init__(self):
        self._types = {}

        self.expires = None
        self._types["ranked_recipients"] = [RankedRecipientsUserList]
        self.ranked_recipients = None
        self.filtered = None
class RankedRecipientsUserList(Response):
    def __init__(self):
        self._types = {}

        self._types["user"] = User
        self.user = None

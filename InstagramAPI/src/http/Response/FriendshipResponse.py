from InstagramAPI.src.http.Response.Objects.FriendshipStatus import FriendshipStatus
from InstagramAPI.src.http.Response.Response import Response


class FriendshipResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["friendship_status"] = FriendshipStatus
        self.friendship_status = None

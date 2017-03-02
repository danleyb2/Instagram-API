from .Response import Response
from .Objects.FriendshipStatus import FrienshipStatus


class FriendshipResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["friendship_status"] = FriendshipStatus
        self.friendship_status = None

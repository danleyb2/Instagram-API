from .Response import Response
from .Objects.FriendshipStatus import FriendshipStatus


class FriendshipsShowManyResponse(Response):
    def __init__(self):
        self._types = {}
        self._types["friendship_statuses"] = [FriendshipStatus]
        self.friendship_statuses = []

from InstagramAPI.src.http.Response.Objects.FriendshipStatus import FriendshipStatus
from InstagramAPI.src.http.Response.Response import Response


class FriendshipsShowManyResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["friendship_statuses"] = [FriendshipStatus]
        self.friendship_statuses = []

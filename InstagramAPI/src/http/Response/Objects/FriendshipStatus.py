from InstagramAPI.src.http.Response.Response import Response


class FriendshipStatus(Response):
    def __init__(self):
        self._types = {}

        self.following = None
        self.followed_by = None
        self.incoming_request = None
        self.outgoing_request = None
        self.is_private = None
        self.is_blocking_reel = None
        self.is_muting_reel = None
        self.blocking = None

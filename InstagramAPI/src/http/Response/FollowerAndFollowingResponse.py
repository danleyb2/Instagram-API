from .Response import Response
from .Objects.User import User


class FollowerAndFollowingResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["users"] = [User]
        self.users = None
        self.next_max_id = None

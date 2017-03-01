from .Response import Response
from .Objects.User import User


class UsernameInfoResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["user"] = User
        self.user = None

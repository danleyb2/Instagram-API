from .Response import Response
from .Objects.User import User


class autoCompleteUserListResponse(Response):
    def __init__(self):
        self._types = {}

        self.expires = None
        self._types["users"] = [User]
        self.users = None

from .Response import Response
from .Objects.User import User


class SearchUserResponse(Response):
    def __init__(self):
        self._types = {}

        self.has_more = None
        self.num_results = None
        self.next_max_id = None
        self._types["users"] = [User]
        self.users = None

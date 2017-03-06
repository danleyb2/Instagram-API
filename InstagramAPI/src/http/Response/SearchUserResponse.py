from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Response import Response


class SearchUserResponse(Response):
    def __init__(self):
        self._types = {}

        self.has_more = None
        self.num_results = None
        self._types["next_max_id"] = str
        self.next_max_id = None
        self._types["users"] = [User]
        self.users = None

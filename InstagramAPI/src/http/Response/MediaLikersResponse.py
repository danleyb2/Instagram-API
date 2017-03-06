from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Response import Response


class MediaLikersResponse(Response):
    def __init__(self):
        self._types = {}

        self.user_count = None
        self._types["users"] = [User]
        self.users = None

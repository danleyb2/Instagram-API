from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Response import Response


class Suggestion(Response):
    def __init__(self):
        self._types = {}

        self.media_infos = None
        self.social_context = None
        self.algorithm = None
        self._types["thumbnail_urls"] = [str]
        self.thumbnail_urls = None
        self.value = None
        self.caption = None
        self._types["user"] = User
        self.user = None
        self._types["large_urls"] = [str]
        self.large_urls = None
        self.media_ids = None
        self.icon = None

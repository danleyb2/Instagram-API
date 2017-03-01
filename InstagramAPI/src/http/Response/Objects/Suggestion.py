from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.User import User


class Suggestion(Response):
    def __init__(self):
        self._types = {}

        self.media_infos = None
        self.social_context = None
        self.algorithm = None
        self.thumbnail_urls = None
        self.value = None
        self.caption = None
        self._types["user"] = User
        self.user = None
        self.large_urls = None
        self.media_ids = None
        self.icon = None

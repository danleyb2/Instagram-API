from InstagramAPI.src.http.Response.Objects.Reel import Reel
from InstagramAPI.src.http.Response.Response import Response


class UserStoryFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self.broadcast = None
        self._types["reel"] = Reel
        self.reel = None

from InstagramAPI.src.http.Response.Objects.Reel import Reel
from InstagramAPI.src.http.Response.Response import Response


class ReelsMediaResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["reels_media"] = [Reel]
        self.reels_media = None
        self._types["reels"] = [Reel]
        self.reels = None

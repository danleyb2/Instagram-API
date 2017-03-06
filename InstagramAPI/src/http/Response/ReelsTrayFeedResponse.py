from InstagramAPI.src.http.Response.Objects.Tray import Tray
from InstagramAPI.src.http.Response.Response import Response


class ReelsTrayFeedResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["tray"] = [Tray]
        self.tray = None

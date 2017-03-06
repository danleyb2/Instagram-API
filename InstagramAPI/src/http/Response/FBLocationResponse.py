from InstagramAPI.src.http.Response.Objects.LocationItem import LocationItem
from InstagramAPI.src.http.Response.Response import Response


class FBLocationResponse(Response):
    def __init__(self):
        self._types = {}

        self.has_more = None
        self._types["items"] = [LocationItem]
        self.items = None

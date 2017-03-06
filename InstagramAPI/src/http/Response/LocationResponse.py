from InstagramAPI.src.http.Response.Objects.Location import Location
from InstagramAPI.src.http.Response.Response import Response


class LocationResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["venues"] = [Location]
        self.venues = None
        self._types["request_id"] = str
        self.request_id = None

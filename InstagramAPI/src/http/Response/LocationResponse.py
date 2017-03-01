from InstagramAPI.src.http.Response.Objects.Location import Location
from .Response import Response


class LocationResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["venues"] = [Location]
        self.venues = None
        self.request_id = None

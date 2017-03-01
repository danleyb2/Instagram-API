from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.Location import Location


class LocationItem(Response):
    def __init__(self):
        self._types = {}

        self.media_bundles = None
        self.subtitle = None
        self._types["location"] = [Location]
        self.location = None
        self.title = None

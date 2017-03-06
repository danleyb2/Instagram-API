from InstagramAPI.src.http.Response.Objects.LocationItem import LocationItem
from InstagramAPI.src.http.Response.Response import Response


class Place(Response):
    def __init__(self):
        self._types = {}

        self.position = None
        self._types["place"] = LocationItem
        self.place = None

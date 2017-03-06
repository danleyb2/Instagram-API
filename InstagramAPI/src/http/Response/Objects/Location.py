from InstagramAPI.src.http.Response.Response import Response


class Location(Response):
    def __init__(self):
        self._types = {}

        self.name = None
        self._types["external_id_source"] = str
        self.external_id_source = None
        self.external_source = None
        self.address = None
        self._types["lat"] = float
        self.lat = None
        self._types["lng"] = float
        self.lng = None
        self._types["external_id"] = str
        self.external_id = None
        self._types["facebook_places_id"] = str
        self.facebook_places_id = None
        self.city = None
        self._types["pk"] = str
        self.pk = None

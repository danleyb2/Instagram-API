from InstagramAPI.src.http.Response.Response import Response


class Location(Response):
    def __init__(self):
        self.name = None
        self.external_id_source = None
        self.external_source = None
        self.address = None
        self.lat = None
        self.lng = None
        self.external_id = None
        self.facebook_places_id = None
        self.city = None
        self.pk = None

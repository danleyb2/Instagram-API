from InstagramAPI.src.http.Response.Response import Response


class GeoMediaResponse(Response):
    def __init__(self):
        self._types = {}

        self.geo_media = None

from InstagramAPI.src.http.Response.Response import Response


class GeoMedia(Response):
    def __init__(self):
        self._types = {}

        self._types["media_id"] = str
        self.media_id = None
        self.display_url = None
        self.low_res_url = None
        self._types["lat"] = float
        self.lat = None
        self._types["lng"] = float
        self.lng = None
        self.thumbnail = None

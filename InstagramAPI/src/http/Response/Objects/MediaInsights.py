from InstagramAPI.src.http.Response.Response import Response


class MediaInsights(Response):
    def __init__(self):
        self._types = {}

        self._types["reach_count"] = [str]
        self.reach_count = None
        self.impression_count = None
        self.engagement_count = None

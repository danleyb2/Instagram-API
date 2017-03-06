from InstagramAPI.src.http.Response.Objects.Insights import Insights
from InstagramAPI.src.http.Response.Response import Response


class InsightsResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["instagram_user"] = [Insights]
        self.instagram_user = None

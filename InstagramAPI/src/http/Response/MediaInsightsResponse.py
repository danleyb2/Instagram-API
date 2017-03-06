from InstagramAPI.src.http.Response.Objects.MediaInsights import MediaInsights
from InstagramAPI.src.http.Response.Response import Response


class MediaInsightsResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["media_organic_insights"] = [MediaInsights]
        self.media_organic_insights = None

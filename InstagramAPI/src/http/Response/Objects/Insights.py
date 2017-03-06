from InstagramAPI.src.http.Response.Response import Response


class Insights(Response):
    def __init__(self):
        self._types = {}

        self._types["instagram_insights"] = [instagram_insights]
        self.instagram_insights = None

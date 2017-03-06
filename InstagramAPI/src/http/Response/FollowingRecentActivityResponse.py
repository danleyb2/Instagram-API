from InstagramAPI.src.http.Response.Response import Response


class FollowingRecentActivityResponse(Response):
    def __init__(self):
        self._types = {}

        self.stories = None
        self._types["next_max_id"] = str
        self.next_max_id = None

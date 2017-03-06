from InstagramAPI.src.http.Response.Response import Response


class ExploreResponse(Response):
    def __init__(self):
        self._types = {}

        self.num_results = None
        self.auto_load_more_enabled = None
        self.items = None
        self.more_available = None
        self._types["next_max_id"] = str
        self.next_max_id = None
        self._types["max_id"] = str
        self.max_id = None

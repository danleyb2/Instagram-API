from InstagramAPI.src.http.Response.Objects.Tag import Tag
from InstagramAPI.src.http.Response.Response import Response


class SearchTagResponse(Response):
    def __init__(self):
        self._types = {}

        self.has_more = None
        self.status = None
        self._types["results"] = [Tag]
        self.results = None

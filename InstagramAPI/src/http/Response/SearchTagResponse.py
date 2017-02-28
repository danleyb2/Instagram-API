from .Response import Response
from .Objects.Tag import Tag


class SearchTagResponse(Response):
    def __init__(self):
        self._types = {}

        self.has_more = None
        self.status = None
        self._types["results"] = [Tag]
        self.results = None

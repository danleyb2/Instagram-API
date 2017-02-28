from .Response import Response


class FBLocationResponse(Response):
    def __init__(self):
        self._types = {}

        self.has_more = None
        self._types["items"] = [LocationItem]
        self.items = None

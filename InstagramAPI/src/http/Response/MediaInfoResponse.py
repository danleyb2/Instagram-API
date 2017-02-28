from .Objects.Item import item
from .Response import Response


class MediaInfoResponse(Response):
    def __init__(self):
        self._types = {}

        self.auto_load_more_enabled = None
        self.status = None
        self.num_results = None
        self.more_available = None
        self._types["items"] = [Item]
        self.items = None

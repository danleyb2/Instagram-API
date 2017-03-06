from InstagramAPI.src.http.Response.Response import Response


class ThreadItem(Response):
    def __init__(self):
        self._types = {}

        self._types["item_id"] = str
        self.item_id = None
        self.item_type = None
        self.text = None
        self._types["user_id"] = str
        self.user_id = None
        self.timestamp = None

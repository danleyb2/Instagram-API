from InstagramAPI.src.http.Response.Response import Response


class RowItem(Response):
    def __init__(self):
        self._types = {}

        self.media_count = None
        self.header = None
        self.title = None
        self.channel_type = None
        self._types["channel_id"] = str
        self.channel_id = None
        self.media = None

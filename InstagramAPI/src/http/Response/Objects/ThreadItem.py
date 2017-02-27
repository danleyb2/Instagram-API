from InstagramAPI.src.http.Response.Response import Response


class ThreadItem(Response):
    def __init__(self):
        self.item_id = None
        self.item_type = None
        self.text = None
        self.user_id = None
        self.timestamp = None

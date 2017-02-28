from InstagramAPI.src.http.Response.Response import Response


class Tag(Response):
    def __init__(self):
        self.media_count = None
        self.name = None
        self.__dict__["id"] = None

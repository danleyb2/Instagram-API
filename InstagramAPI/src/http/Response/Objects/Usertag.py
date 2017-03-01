from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.In import In


class Usertag(Response):
    def __init__(self):
        self._types = {}
        self._types["in"] = [In]
        self.__dict__["in"] = None
        self.photo_of_you = None

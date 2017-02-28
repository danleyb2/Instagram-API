from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.Param import Param


class Experiment(Response):
    def __init__(self):
        self._types = {}

        self._types["params"] = [Param]
        self.params = None
        self.group = None
        self.name = None

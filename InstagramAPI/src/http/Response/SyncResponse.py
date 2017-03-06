from InstagramAPI.src.http.Response.Objects.Experiment import Experiment
from InstagramAPI.src.http.Response.Response import Response


class SyncResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["experiments"] = [Experiment]
        self.experiments = None

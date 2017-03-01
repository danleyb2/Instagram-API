from .Response import Response
from .Objects.Experiment import Experiment


class SyncResponse(Response):
    def __init__(self):
        self._types = {}
        self._types["experiments"] = [Experiment]
        self.experiments = None

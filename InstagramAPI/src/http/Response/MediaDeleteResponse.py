from .Response import Response


class MediaDeleteResponse(Response):
    def __init__(self):
        self.did_delete = None

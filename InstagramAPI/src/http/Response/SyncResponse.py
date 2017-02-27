from InstagramAPI.src.http.Response import Response

class SyncResponse(Response):
    def __init__(self):
        self.experiments = None

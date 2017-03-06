from InstagramAPI.src.http.Response.Response import Response


class UploadVideoResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["upload_id"] = str
        self.upload_id = None
        self.message = None

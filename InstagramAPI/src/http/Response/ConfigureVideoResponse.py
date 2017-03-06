from InstagramAPI.src.http.Response.Response import Response


class ConfigureVideoResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["upload_id"] = str
        self.upload_id = None
        self._types["media_id"] = str
        self.media_id = None
        self.image_url = None
        self.video_version = None

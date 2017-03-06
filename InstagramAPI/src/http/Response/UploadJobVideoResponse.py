from InstagramAPI.src.http.Response.Response import Response


class UploadJobVideoResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["upload_id"] = str
        self.upload_id = None
        self.video_upload_urls = None

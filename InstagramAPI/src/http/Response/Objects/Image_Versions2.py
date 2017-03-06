from InstagramAPI.src.http.Response.Objects.HdProfilePicUrlInfo import HdProfilePicUrlInfo
from InstagramAPI.src.http.Response.Response import Response


class Image_Versions2(Response):
    def __init__(self):
        self._types = {}

        self._types["candidates"] = [HdProfilePicUrlInfo]
        self.candidates = None

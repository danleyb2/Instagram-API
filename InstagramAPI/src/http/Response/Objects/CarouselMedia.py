from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.Image_Versions2 import Image_Versions2
from InstagramAPI.src.http.Response.Objects.VideoVersions import VideoVersions


class CarouselMedia(Response):
    PHOTO = 1
    VIDEO = 2

    def __init__(self):
        self._types = {}

        self._types["pk"] = str
        self.pk = None
        self._types["id"] = str
        self.id = None
        self._types["carousel_parent_id"] = str
        self.carousel_parent_id = None
        self._types["image_versions2"] = Image_Versions2
        self.image_versions2 = None
        self._types["video_versions"] = [VideoVersions]
        self.video_versions =  None
        self.has_audio = False
        self.video_duration = ''
        self.original_height = None
        self.original_width = None
        self.media_type = None

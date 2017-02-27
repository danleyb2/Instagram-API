from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.Caption import Caption
from InstagramAPI.src.http.Response.Objects.CarouselMedia import CarouselMedia
from InstagramAPI.src.http.Response.Objects.Comment import Comment
from InstagramAPI.src.http.Response.Objects.Explore import Explore
from InstagramAPI.src.http.Response.Objects.Image_Versions2 import Image_Versions2
from InstagramAPI.src.http.Response.Objects.Media import Media
from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Objects.Usertag import Usertag
from InstagramAPI.src.http.Response.Objects.VideoVersions import VideoVersions


class Item(Response):
    PHOTO = 1
    VIDEO = 2
    ALBUM = 8

    def __init__(self):
        self._types = {}

        self.taken_at = None
        self.pk = None
        self.id = None
        self.device_timestamp = None
        self.media_type = None
        self.code = None
        self.client_cache_key = None
        self.filter_type = None
        self._types["image_versions2"] = Image_Versions2
        self.image_versions2 = None
        self.original_width = None
        self.original_height = None
        self.view_count = 0
        self.organic_tracking_token = None
        self.has_more_comments = None
        self.max_num_visible_preview_comments = None
        self.preview_comments = None
        self.reel_mentions = None
        self.story_cta = None
        self.caption_position = None
        self.expiring_at = None
        self.is_reel_media = None
        self.next_max_id =  None
        self._types["carousel_media"] = [CarouselMedia]
        self.carousel_media = None
        self._types["comments"] = [Comment]
        self.comments = None
        self.comment_count = 0
        self._types["caption"] = Caption
        self.caption = None
        self.caption_is_edited = None
        self.photo_of_you = None
        self._types["video_versions"] = [VideoVersions]
        self.video_versions = None
        self.has_audio = False
        self.video_duration = ''
        self._types["user"] = User
        self.user = None
        self._types["likers"] = [User]
        self.likers = ''
        self.like_count = 0
        self._types["preview"] = [str]
        self.preview = ''
        self.has_liked = False
        self.explore_context = ''
        self.explore_source_token = ''
        self._types["explore"] = Explore
        self.explore = ''
        self.impression_token = ''
        self._types["usertags"] = Usertag
        self.usertags = None
        self.media_or_ad = None
        self._types["media"] = Media
        self.media = None
        self.stories = None
        self.top_likers = None

    def setMediaOrAd(self, params):
        for k in params:
            self.__dict__[k] = params[k]

    def getItemUrl(self):
        return 'https://www.instagram.com/p/' + self.getCode() + '/'

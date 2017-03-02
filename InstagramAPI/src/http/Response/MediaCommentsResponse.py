from InstagramAPI.src.http.Response.Objects.Comment import Comment
from InstagramAPI.src.http.Response.Objects.Caption import Caption
from .Response import Response


class MediaCommentsResponse(Response):
    def __init__(self, response):
        self._types = {}

        self._types = [Comment]
        self.comments = []
        self.comment_count = None
        self.comment_likes_enabled = None
        self._types["next_max_id"] = str
        self.next_max_id = None
        self._types["caption"] = Caption
        self.caption = None
        self.has_more_comments = None
        self.caption_is_edited = None
        self.preview_comments = None

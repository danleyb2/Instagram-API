from InstagramAPI.src.http.Response.Response import Response
from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Objects.ThreadItem import ThreadItem


class Thread(Response):
    def __init__(self):
        self._types = {}

        self.named = None
        self._types["users"] = [User]
        self.users = None
        self.has_newer = None
        self.viewer_id = None
        self.thread_id = None
        self.last_activity_at = None
        self.newest_cursor = None
        self.is_spam = None
        self.has_older = None
        self.oldest_cursor = None
        self._types["left_users"] = [User]
        self.left_users = None
        self.muted = None
        self._types["items"] = [ThreadItem]
        self.items = None
        self.thread_type = None
        self.thread_title = None
        self.canonical = None
        self._types["inviter"] = User
        self.inviter = None
        self.pending = None

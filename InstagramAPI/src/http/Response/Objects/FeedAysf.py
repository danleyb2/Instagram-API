from InstagramAPI.src.http.Response.Objects.Suggestion import Suggestion
from InstagramAPI.src.http.Response.Response import Response


class FeedAysf(Response):
    def __init__(self):
        self._types = {}

        self.landing_site_type = None
        self._types["uuid"] = str
        self.uuid = None
        self.view_all_text = None
        self.feed_position = None
        self.landing_site_title = None
        self.is_dismissable = None
        self._types["suggestions"] = [Suggestion]
        self.suggestions = None
        self.should_refill = None
        self.display_new_unit = None
        self.fetch_user_details = None
        self.title = None

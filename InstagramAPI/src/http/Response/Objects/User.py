from InstagramAPI.src.http.Response.Objects.FriendshipStatus import FriendshipStatus
from InstagramAPI.src.http.Response.Response import Response


class User(Response):
    def __init__(self):
        self._types = {}

        self.username = None
        self.has_anonymous_profile_picture = False
        self.is_favorite = False
        self.profile_pic_url = None
        self.full_name = None
        self._types["pk"] = str
        self.pk = None
        self.is_verified = False
        self.is_private = False
        self.coeff_weight = 0
        self._types["friendship_status"] = FriendshipStatus
        self.friendship_status = None
        self.hd_profile_pic_versions = None
        self.byline = None
        self.search_social_context = None
        self.unseen_count = None
        self.mutual_followers_count = None
        self.follower_count = None
        self.social_context = None
        self.media_count = None
        self.following_count = None
        self.is_business = None
        self.usertags_count = None
        self.profile_context = None
        self.biography = None
        self.geo_media_count = None
        self.is_unpublished = None
        self.allow_contacts_sync = None # // login prop
        self.show_feed_biz_conversion_icon = None # // login prop
        self._types["profile_pic_id"] = str
        self.profile_pic_id = None # // Ranked recipents response prop
        self.auto_expand_chaining = None # // getUsernameInfo prop
        self.can_boost_post = None # // getUsernameInfo prop
        self.is_profile_action_needed = None # // getUsernameInfo prop
        self.has_chaining = None # // getUsernameInfo prop
        self.include_direct_blacklist_status = None # // getUsernameInfo prop
        self.can_see_organic_insights = None # // getUsernameInfo prop
        self.can_convert_to_business = None # // getUsernameInfo prop
        self.show_business_conversion_icon = None # // getUsernameInfo prop
        self.show_conversion_edit_entry = None # // getUsernameInfo prop
        self.show_insights_terms = None # // getUsernameInfo prop
        self.hd_profile_pic_url_info = None # // getUsernameInfo prop
        self.usertag_review_enabled = None # // getUsernameInfo prop
        self.is_needy = None # // getUsernameInfo prop
        self.external_url = None # // getUsernameInfo prop
        self.external_lynx_url = None # // getUsernameInfo prop

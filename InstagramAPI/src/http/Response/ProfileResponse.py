from InstagramAPI.src.http.Response.Response import Response


class ProfileResponse(Response):
    def __init__(self):
        self._types = {}

        self.username = None
        self.phone_number = None
        self.has_anonymous_profile_picture = None
        self.hd_profile_pic_versions = None
        self.gender = None
        self.birthday = None
        self.needs_email_confirm = None
        self.national_number = None
        self.profile_pic_url = None
        self._types["profile_pic_id"] = str
        self.profile_pic_id = None
        self.biography = None
        self.full_name = None
        self._types["pk"] = str
        self.pk = None
        self.country_code = None
        self.hd_profile_pic_url_info = None
        self.email = None
        self.is_private = None
        self.external_url = None

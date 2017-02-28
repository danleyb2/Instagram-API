from .Response import Response
from .Objects.User import User


class LoginResponse(Response):
    def __init__(self):
        self._types = {}

        self.username = None
        self.has_anonymous_profile_picture = None
        self.profile_pic_url = None
        self.profile_pic_id = None
        self.full_name = None
        self.pk = None
        self.is_private = None
        self.error_title = None # // on wrong pass
        self.error_type = None # // on wrong pass
        self.buttons = None # // on wrong pass
        self.invalid_credentials = None # // on wrong pass
        self._types["logged_in_user"] = User
        self.logged_in_user = None

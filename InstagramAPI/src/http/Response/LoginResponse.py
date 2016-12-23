from Response import Response


class LoginResponse(Response):
    def __init__(self, response):

        self.username = None
        self.has_anonymous_profile_picture = None
        self.profile_pic_url = None
        self.profile_pic_id = None
        self.full_name = None
        self.pk = None
        self.is_private = None

        if 'logged_in_user' in response and 'username' in response['logged_in_user']:
            self.username = response['logged_in_user']['username']
            self.has_anonymous_profile_picture = response['logged_in_user']['has_anonymous_profile_picture']
            self.profile_pic_url = response['logged_in_user']['profile_pic_url']
            self.full_name = response['logged_in_user']['full_name']
            self.pk = response['logged_in_user']['pk']
            self.is_private = response['logged_in_user']['is_private']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUsername(self):
        return self.username

    def getHasAnonymousProfilePicture(self):
        return self.has_anonymous_profile_picture

    def getProfilePicUrl(self):
        return self.profile_pic_url

    def getProfilePicId(self):
        return self.profile_pic_id

    def getFullName(self):
        return self.full_name

    def getUsernameId(self):
        return str(self.pk)

    def getIsPrivate(self):
        return self.is_private

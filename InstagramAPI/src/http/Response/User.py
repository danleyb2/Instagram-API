class User(object):
    def __init__(self, userData):
        self.username = None
        self.profile_pic_url = None
        self.full_name = None
        self.pk = None
        self.is_verified = None
        self.is_private = None

        self.username = userData['username']
        self.profile_pic_url = userData['profile_pic_url']
        self.full_name = userData['full_name']
        self.pk = userData['pk']
        self.is_verified = userData['is_verified']
        self.is_private = userData['is_private']

    def getUsername(self):
        return self.username

    def getProfilePicUrl(self):
        return self.profile_pic_url

    def getFullName(self):
        return self.full_name

    def getUsernameId(self):
        return self.pk

    def isVerified(self):
        return self.is_verified

    def isPrivate(self):
        return self.is_private

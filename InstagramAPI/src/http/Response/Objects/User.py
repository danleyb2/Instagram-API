from InstagramAPI.src.http.Response.Objects.FriendshipStatus import FriendshipStatus


class User(object):
    def __init__(self, userData):
        self.username = None
        self.has_anonymous_profile_picture = False
        self.is_favorite = False
        self.profile_pic_url = None
        self.full_name = None
        self.pk = None
        self.is_verified = False
        self.is_private = False
        self.coeff_weight = 0
        self.friendship_status = None

        self.username = userData['username']
        self.profile_pic_url = userData['profile_pic_url']
        self.full_name = userData['full_name']
        self.pk = userData['pk']
        if 'is_verified' in userData and userData['is_verified']:
            self.is_verified = userData['is_verified']
        self.is_private = userData['is_private']
        if 'has_anonymous_profile_picture' in userData and userData['has_anonymous_profile_picture']:
            self.has_anonymous_profile_picture = userData['has_anonymous_profile_picture']
        if 'is_favorite' in userData and userData['is_favorite']:
            self.is_favorite = userData['is_favorite']
        if 'coeff_weight' in userData and userData['coeff_weight']:
            self.coeff_weight = userData['coeff_weight']
        if 'friendship_status' in userData and userData['friendship_status']:
            self.friendship_status = FriendshipStatus(userData['friendship_status'])

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

    def hasAnonymousProfilePicture(self):
        return self.has_anonymous_profile_picture

    def isFavorite(self):
        return self.is_favorite

    def getCoeffWeight(self):
        return self.coeff_weight

    def getFriendshipStatus(self):
        return self.friendship_status

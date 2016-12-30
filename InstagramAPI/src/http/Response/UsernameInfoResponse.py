from InstagramAPI.src.http.Response.HdProfilePicUrlInfo import HdProfilePicUrlInfo
from Response import Response


class UsernameInfoResponse(Response):
    def __init__(self, response):

        self.usertags_count = None
        self.has_anonymous_profile_picture = None
        self.full_name = None
        self.following_count = None
        self.auto_expand_chaining = None
        self.external_lynx_url = ''
        self.can_boost_post = False
        self.hd_profile_pic_versions = None
        self.biography = None
        self.has_chaining = None
        self.media_count = None
        self.follower_count = None
        self.pk = None
        self.username = None
        self.geo_media_count = None
        self.profile_pic_url = None
        self.can_see_organic_insights = False
        self.is_private = None
        self.can_convert_to_business = False
        self.is_business = None
        self.show_insights_terms = False
        self.hd_profile_pic_url_info = None
        self.usertag_review_enabled = False
        self.external_url = None

        if self.STATUS_OK == response['status']:
            self.usertags_count = response['user']['usertags_count']
            self.has_anonymous_profile_picture = response['user']['has_anonymous_profile_picture']
            self.full_name = response['user']['full_name']
            self.following_count = response['user']['following_count']
            self.auto_expand_chaining = response['user']['auto_expand_chaining']
            if 'external_lynx_url' in response['user']:
                self.external_lynx_url = response['user']['external_lynx_url']

            if 'can_boost_post' in response['user']:
                self.can_boost_post = response['user']['can_boost_post']

            if 'hd_profile_pic_versions' in response['user']:
                profile_pics_vers = []
                for profile_pic in response['user']['hd_profile_pic_versions']:
                    profile_pics_vers.append(HdProfilePicUrlInfo(profile_pic))

                self.hd_profile_pic_versions = profile_pics_vers

            self.biography = response['user']['biography']
            self.has_chaining = response['user']['has_chaining']
            self.media_count = response['user']['media_count']
            self.follower_count = response['user']['follower_count']
            self.pk = response['user']['pk']
            self.username = response['user']['username']
            self.geo_media_count = response['user']['geo_media_count']
            self.profile_pic_url = response['user']['profile_pic_url']
            if 'can_see_organic_insights' in response['user']:
                self.can_see_organic_insights = response['user']['can_see_organic_insights']

            self.is_private = response['user']['is_private']
            if 'can_convert_to_business' in response['user']:
                self.can_convert_to_business = response['user']['can_convert_to_business']

            self.is_business = response['user']['is_business']
            if 'show_insights_terms' in response['user']:
                self.show_insights_terms = response['user']['show_insights_terms']

            self.hd_profile_pic_url_info = HdProfilePicUrlInfo(response['user']['hd_profile_pic_url_info'])
            if 'usertag_review_enabled' in response['user']:
                self.usertag_review_enabled = response['user']['usertag_review_enabled']

            self.external_url = response['user']['external_url']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUsertagCount(self):
        return self.usertags_count

    def getHasAnonymousProfilePicture(self):
        return self.has_anonymous_profile_picture

    def getFullName(self):
        return self.full_name

    def getFollowingCount(self):
        return self.following_count

    def autoExpandChaining(self):
        return self.auto_expand_chaining

    def getExternalLynxUrl(self):
        return self.external_lynx_url

    def canBoostPost(self):
        return self.can_boost_post

    def getProfilePicVersions(self):
        return self.hd_profile_pic_versions

    def getBiography(self):
        return self.biography

    def hasChaining(self):
        return self.has_chaining

    def getMediaCount(self):
        return self.media_count

    def getFollowerCount(self):
        return self.follower_count

    def getUsernameId(self):
        return self.pk

    def getUsername(self):
        return self.username

    def getGeoMediaCount(self):
        return self.geo_media_count

    def getProfilePicUrl(self):
        return self.profile_pic_url

    def canSeeOrganicInsights(self):
        return self.can_see_organic_insights

    def isPrivate(self):
        return self.is_private

    def canConvertToBusiness(self):
        return self.can_convert_to_business

    def isBusiness(self):
        return self.is_business

    def showInsightsTerms(self):
        return self.show_insights_terms

    def getHdProfilePicUrlInfo(self):
        return self.hd_profile_pic_url_info

    def getUsertagReviewEnabled(self):
        return self.usertag_review_enabled

    def getExternalUrl(self):
        return self.external_url

from InstagramAPI.src.http.Response.Objects.HdProfilePicUrlInfo import HdProfilePicUrlInfo
from .Response import Response


class ProfileResponse(Response):
    def __init__(self, response):
        self.username = None
        self.phone_number = None
        self.has_anonymous_profile_picture = None
        self.hd_profile_pic_versions = None
        self.gender = None
        self.birthday = None
        self.needs_email_confirm = None
        self.national_number = None
        self.profile_pic_url = None
        self.profile_pic_id = None
        self.biography = None
        self.full_name = None
        self.pk = None
        self.country_code = None
        self.hd_profile_pic_url_info = None
        self.email = None
        self.is_private = None
        self.external_url = None

        if self.STATUS_OK == response['status']:
            for p, v in response['user'].iteritems():
                setattr(self, p, v)

            self.hd_profile_pic_url_info = HdProfilePicUrlInfo(self.hd_profile_pic_url_info)
            if self.hd_profile_pic_versions:
                profile_pics_vers = []
                for profile_pic in self.hd_profile_pic_versions:
                    profile_pics_vers.append(HdProfilePicUrlInfo(profile_pic))
                self.hd_profile_pic_versions = profile_pics_vers
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUsername(self):
        return self.username

    def getPhoneNumber(self):
        return self.phone_number

    def hasAnonymousProfilePicture(self):
        return self.has_anonymous_profile_picture

    def getHdProfilePicVersions(self):
        return self.hd_profile_pic_versions

    def getGender(self):
        return self.gender

    def getBirthday(self):
        return self.birthday

    def needsEmailConfirm(self):
        return self.needs_email_confirm

    def getNationalNumber(self):
        return self.national_number

    def getProfilePicUrl(self):
        return self.profile_pic_url

    def getProfilePicId(self):
        return self.profile_pic_id

    def getBiography(self):
        return self.biography

    def getFullName(self):
        return self.full_name

    def getUsernameId(self):
        return self.pk

    def getCountryCode(self):
        return self.country_code

    def getHdProfilePicUrlInfo(self):
        return self.hd_profile_pic_url_info

    def getEmail(self):
        return self.email

    def isPrivate(self):
        return self.is_private

    def getExternalUrl(self):
        return self.external_url

from HdProfilePicUrlInfo import HdProfilePicUrlInfo
from Response import Response


class AccountCreationResponse(Response):
    def __init__(self, response):

        self.username = None
        self.has_anonymous_profile_picture = None
        self.allow_contacts_sync = None
        self.nux_private_first_page = None
        self.profile_pic_url = None
        self.full_name = None
        self.pk = None
        self.hd_profile_pic_url_info = None
        self.nux_private_enabled = None
        self.is_private = None
        self.account_created = False
        self.feedback_title = ''
        self.feedback_message = ''
        self.spam = False
        self.feedback_action = ''
        self.feedback_url = ''
        self.errors = None

        if (self.STATUS_OK == response['status']) and ('errors' not in response):

            self.username = response['created_user']['username']
            self.has_anonymous_profile_picture = response['created_user']['has_anonymous_profile_picture']
            self.allow_contacts_sync = response['created_user']['allow_contacts_sync']
            self.nux_private_first_page = response['created_user']['nux_private_first_page']
            self.profile_pic_url = response['created_user']['profile_pic_url']
            self.full_name = response['created_user']['full_name']
            self.pk = response['created_user']['pk']
            self.hd_profile_pic_url_info = HdProfilePicUrlInfo(response['created_user']['hd_profile_pic_url_info'])
            self.nux_private_enabled = response['created_user']['nux_private_enabled']
            self.is_private = response['created_user']['is_private']
            self.account_created = response['account_created']
        else:
            if 'message' in response:
                self.setMessage(response['message'])

            if 'errors' in response:
                self.errors = response['errors']

            if not self.errors:
                self.feedback_title = response['feedback_title']
                self.feedback_message = response['feedback_message']
                self.spam = response['spam']
                self.feedback_action = response['feedback_action']
                self.feedback_url = response['feedback_url']

        self.setStatus(response['status'])

    def hasAnonymousProfilePicture(self):
        return self.has_anonymous_profile_picture

    def allowContactsSync(self):
        return self.allow_contacts_sync

    def nuxPrivateFirstPage(self):
        return self.nux_private_first_page

    def getProfilePicUrl(self):
        return self.profile_pic_url

    def getFullName(self):
        return self.full_name

    def getUsernameId(self):
        return self.pk

    def getHdProfilePicUrlInfo(self):
        return self.hd_profile_pic_url_info

    def isNuxPrivateEnabled(self):
        return self.nux_private_enabled

    def isPrivate(self):
        return self.is_private

    def isAccountCreated(self):
        return self.account_created

    def getFeedbackTitle(self):
        return self.feedback_title

    def getFeedbackMessage(self):
        return self.feedback_message

    def isSpam(self):
        return self.spam

    def getFeedbackAction(self):
        return self.feedback_action

    def getFeedbackUrl(self):
        return self.feedback_url

    def getErrors(self):
        return self.errors

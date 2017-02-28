import json
import locale
import re
import time
import urllib
from collections import OrderedDict
from distutils.version import LooseVersion

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from .Utils import *
from .http import HttpInterface, UserAgent
from .http.Response import *

from .InstagramException import InstagramException
from .Constants import Constants
from .SignatureUtils import SignatureUtils

locale.setlocale(locale.LC_NUMERIC, '')


class Instagram:
    instance = None

    def __init__(self, debug=False, IGDataPath=None, truncatedDebug=False):

        """
        Default class constructor.
        :param debug: Debug on or off, False by default.
        """
        Instagram.instance = self
        self.username = None  # // Instagram username
        self.password = None  # // Instagram password
        self.debug = None  # // Debug
        self.truncatedDebug = None

        self.uuid = None  # // UUID
        self.device_id = None  # // Device ID
        self.username_id = None  # // Username ID
        self.token = None  # // _csrftoken
        self.isLoggedIn = False  # // Session status
        self.rank_token = None  # // Rank token
        self.IGDataPath = None  # // Data storage path
        self.customPath = False
        self.http = None
        self.settings = None
        self.proxy = None  # Full Proxy
        self.proxyHost = None  # Proxy Host and Port
        self.proxyAuth = None  # Proxy User and Pass

        self.debug = debug
        self.truncatedDebug = truncatedDebug


        if IGDataPath is not None:
            self.IGDataPath = IGDataPath
            self.customPath = True
        else:
            self.IGDataPath = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
                username,
                ''
            )
            if not os.path.isdir(self.IGDataPath):
                os.mkdir(self.IGDataPath, 0o777)

    def setUser(self, username, password):
        """
         Set the user. Manage multiple accounts.

        :type username: str
        :param username: Your Instagram username.
        :type password: str
        :param password: Your Instagram password.
        :
        """
        self.device_id = SignatureUtils.generateDeviceId(hashlib.md5((username + password).encode("utf-8")))

        self.username = username
        self.password = password

        self.checkSettings(username)

        self.http = HttpInterface(self)

        self.uuid = SignatureUtils.generateUUID(True)

        if os.path.isfile(self.IGDataPath + self.username + '-cookies.dat') and \
                (self.settings.get('username_id') != None) and \
                (self.settings.get('token') != None):
            self.isLoggedIn = True
            self.username_id = self.settings.get('username_id')
            self.rank_token = str(self.username_id) + '_' + self.uuid
            self.token = self.settings.get('token')
        else:
            self.isLoggedIn = False

    def checkSettings(self, username):
        if not self.customPath:
            self.IGDataPath = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
                username,
                ''
            )

        if not os.path.isdir(self.IGDataPath): os.mkdir(self.IGDataPath, 0o777)

        self.settings = Settings(
            os.path.join(self.IGDataPath, 'settings-' + username + '.dat')
        )
        if self.settings.get('version') is None:
            self.settings.set('version', Constants.VERSION)

        if (self.settings.get('user_agent') is None) or (
                    LooseVersion(self.settings.get('version')) < LooseVersion(Constants.VERSION)):
            userAgent = UserAgent(self)
            ua = userAgent.buildUserAgent()
            self.settings.set('version', Constants.VERSION)
            self.settings.set('user_agent', ua)

    def setProxy(self, proxy, port=None, username=None, password=None):
        """
        Set the proxy.

        :type proxy: str
        :param proxy: Full proxy string. Ex: user:pass@192.168.0.0:8080
                        Use $proxy = "" to clear proxy
        :type port: int
        :param port: Port of proxy
        :type username: str
        :param username: Username for proxy
        :type password: str
        :param password: Password for proxy

        :raises: InstagramException
        """
        self.proxy = proxy

        if proxy == '':
            return

        proxy = parse_url(proxy)

        if port and isinstance(port, int):
            proxy['port'] = int(port)

        if username and password:
            proxy['user'] = username
            proxy['pass'] = password

        if proxy['host'] and proxy['port'] and isinstance(proxy['port'], int):
            self.proxyHost = proxy['host'] + ':' + proxy['port']
        else:
            raise InstagramException('Proxy host error. Please check ip address and port of proxy.')

        if proxy['user'] and proxy['pass']:
            self.proxyAuth = proxy['user'] + ':' + proxy['pass']

    def login(self, force=False):
        """
        Login to Instagram.

        :type force: bool
        :param force: Force login to Instagram, this will create a new session
        :return: Login data
        :rtype List:
        """
        if (not self.isLoggedIn) or force:
            self.syncFeatures(True)

            response = (
                self.request('si/fetch_headers')
                .requireLogin(True)
                .addParams('challenge_type', 'signup')
                .addParams('guid', SignatureUtils.generateUUID(False))
                .getResponse(ChallengeResponse(), True)
            )

            token = re.search(r'^Set-Cookie: csrftoken=([^;]+)', response.getFullResponse()[0], re.MULTILINE)
            if not token:
                raise InstagramException('Missing csfrtoken', ErrorCode.INTERNAL_CSRF_TOKEN_ERROR)

            response = (
                self.request('accounts/login/')
                .requireLogin(True)
                .addPost('phone_id', SignatureUtils.generateUUID(True))
                .addPost('_csrftoken', token[0])
                .addPost('username', self.username)
                .addPost('guid', self.uuid)
                .addPost('device_id', self.device_id)
                .addPost('password', self.password)
                .addPost('login_attempt_count', 0)
                .getResponse(LoginResponse(), True)
            )

            self.isLoggedIn = True
            self.username_id = response.getLoggedInUser().getPk()
            self.settings.set('username_id', str(self.username_id))
            self.rank_token = str(self.username_id) + '_' + self.uuid
            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', response.getFullResponse()[0], re.MULTILINE)
            if match: self.token = match.group(1)
            self.settings.set('token', self.token)
            self.settings.set('last_login', str(int(time.time())))

            self.syncFeatures()
            self.autoCompleteUserList()
            self.timelineFeed()
            self.getRankedRecipients()
            self.getRecentRecipients()
            self.megaphoneLog()
            self.getv2Inbox()
            self.getRecentActivity()
            self.getReelsTrayFeed()

            return self.explore()

        if self.settings.get('last_login') is None:
            self.settings.set('last_login', str(int(time.time())))

        check = self.timelineFeed()
        if check.getMessage() == 'login_required':
            self.login(True)
        if ((int(time.time()) - int(self.settings.get('last_login'))) > 1800):
            self.settings.set('last_login', str(int(time.time())))

            self.autoCompleteUserList()
            self.getReelsTrayFeed()
            self.getRankedRecipients()
            # push register
            self.getRecentRecipients()
            # push register
            self.megaphoneLog()
            self.getv2Inbox()
            self.getRecentActivity()

            return self.explore()

    def syncFeatures(self, prelogin=False):
        if prelogin:
            return (
                self.request('qe/sync/')
                .requireLogin(True)
                .addPost('id', SignatureUtils.generateUUID(True))
                .addPost('experiments', Constants.LOGIN_EXPERIMENTS)
                .getResponse(SyncResponse())
            )
        else:
            return (
                self.request('qe/sync/')
                .addPost('_uuid', self.uuid)
                .addPost('_uid', self.username_id)
                .addPost('_csrftoken', self.token)
                .addPost('id', self.username_id)
                .addPost('experiments', Constants.EXPERIMENTS)
                .getResponse(SyncResponse())
            )

    def autoCompleteUserList(self):
        (self.request('friendships/autocomplete_user_list/')
         .setCheckStatus(False)
         .addParams('version', '2')
         .getResponse(autoCompleteUserListResponse()))

    def pushRegister(self, gcmToken):
        deviceToken = json.dumps(
            OrderedDict([
                ('k', gcmToken),
                ('v', 0),
                ('t', 'fbns-b64')
            ])
        )
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('guid', self.uuid),
                ('phone_id', SignatureUtils.generateUUID(True)),
                ('device_type', 'android_mqtt'),
                ('device_token', deviceToken),
                ('is_main_push_channel', True),
                ('_csrftoken', self.token),
                ('users', self.username_id)
            ])
        )
        return self.http.request(
            'push/register/?platform=10&device_type=android_mqtt',
            SignatureUtils.generateSignature(data)
        )[1]

    def timelineFeed(self, maxId=None):
        request = (
            self.request('feed/timeline')
            .addParams('rank_token', self.rank_token)
            .addParams('ranked_content', True)
        )
        if maxId is not None:
            request.addParams('max_id', maxId)

        return request.getResponse(TimelineFeedResponse())

    def megaphoneLog(self):
        return (
            self.request('megaphone/log/')
            .setSignedPost(False)
            .addPost('type', 'feed_aysf')
            .addPost('action', 'seen')
            .addPost('reason', '')
            .addPost('_uuid', self.uuid)
            .addPost('device_id', self.device_id)
            .addPost('_csrftoken', self.token)
            .addPost('uuid', hashlib.md5(str(int(time.time())).encode("utf-8")).hexdigest())
            .getResponse(MegaphoneLogResponse())
        )

    def getPendingInbox(self):
        """
        Pending Inbox

        :rtype: object
        :return: Pending Inbox Data
        """
        return self.request('direct_v2/pending_inbox').getResponse(PendingInboxResponse())

    def getRankedRecipients(self):
        """
        Ranked recipients.

        :rtype:list
        :return: Ranked recipients Data
        """
        return (
            self.request('direct_v2/ranked_recipients')
            .addParams('show_threads', True)
            .getResponse(RankedRecipientsResponse())
        )

    def getRecentRecipients(self):
        """
        Recent recipients.

        :rtype: list
        :return: Ranked recipients Data
        """
        return (
            self.request('direct_share/recent_recipients/')
            .getResponse(RecentRecipientsResponse())
        )

    def explore(self):
        """
        Explore Tab

        :rtype: object
        :return: Explore data
        """
        return self.request('discover/explore/').getResponse(ExploreResponse())

    def expose(self):
        return (
            self.request('qe/expose/')
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('id', self.username_id)
            .addPost('_csrftoken', self.token)
            .addPost('experiment', 'ig_android_profile_contextual_feed')
            .getResponse(ExposeResponse())
        )

    def logout(self):
        """
        Logout of Instagram.

        :rtype: bool
        :return: Returns true if logged out correctly
        """
        return self.request('accounts/logout/').getResponse(LogoutResponse())

    def uploadPhoto(self, photo, caption=None, upload_id=None, customPreview=None, location=None, filter_=None):
        """
        Upload photo to Instagram.

        :type photo: str
        :param photo: Path to your photo
        :type caption: str
        :param caption: Caption to be included in your photo.
        :rtype: object
        :return: Upload data
        """
        return self.http.uploadPhoto(photo, caption, upload_id, customPreview, location, filter_)

    def uploadPhotoStory(self, photo, caption=None, upload_id=None, customPreview=None):
        return self.http.uploadPhoto(photo, caption, upload_id, customPreview, None, None, True)

    def uploadVideo(self, video, caption=None, customPreview=None):
        """
        Upload video to Instagram.

        :type video: str
        :param photo: Path to your video
        :type caption: str
        :param caption: Caption to be included in your video.
        :rtype: object
        :return: Upload data
        """
        return self.http.uploadVideo(video, caption, customPreview)

    def direct_share(self, media_id, recipients, text=None):
        self.http.direct_share(media_id, recipients, text)

    def direct_message(self, recipients, text):
        """
        Send direct message to user by inbox.

        :type recipients: list|int
        :param recipients: Users id
        :type text: str
        :param text: Text message

        :return: void
        """
        self.http.direct_message(recipients, text)

    def directThread(self, threadId):
        """
        Direct Thread Data

        :type threadId: str
        :param threadId: Thread Id
        :rtype: object
        :return: Direct Thread Data
        """
        directThread = self.http.request("direct_v2/threads/" + str(threadId) + "/?")[1]

        if directThread['status'] != 'ok':
            raise InstagramException(directThread['message'] + "\n")
            # return Fixme unreachable code

        return directThread

    def directThreadAction(self, threadId, threadAction):
        """
        Direct Thread Action

        :type threadId: str
        :param threadId: Thread Id
        :type threadAction: str
        :param threadAction: Thread Action 'approve' OR 'decline' OR 'block'
        :rtype: object
        :return: Direct Thread Action Data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token)
            ])
        )
        return self.request(
            "direct_v2/threads/" + str(threadId) + "/" + str(threadAction) + "/",
            self.generateSignature(data)  # todo Unresolved reference
        )[1]

    def configureVideo(self, upload_id, video, caption='', customPreview=None):

        self.uploadPhoto(video, caption, upload_id, customPreview)
        size = Image.open(video).size[0]

        return (
            self.request('media/configure/')
            .addParams('video', 1)
            .addPost('upload_id', upload_id)
            .addPost('source_type', '3')
            .addPost('poster_frame_index', 0)
            .addPost('length', 0.00)
            .addPost('audio_muted', False)
            .addPost('filter_type', '0')
            .addPost('video_result', 'deprecated')
            .addPost('clips', OrderedDict([
                ('length',          Utils.getSeconds(video)),
                ('source_type',     '3'),
                ('camera_position', 'back')
            ]))
            .addPost('extra', OrderedDict([
                ('source_width',  960),
                ('source_height', 1280)
            ]))
            .addPost('device', OrderedDict([
                ('manufacturer',     self.settings.get('manufacturer')),
                ('model',            self.settings.get('model')),
                ('android_version',  Constants.ANDROID_VERSION),
                ('android_release',  Constants.ANDROID_RELEASE)
            ]))
            .addPost('_csrftoken', self.token)
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('caption', caption)
            .setReplacePost({'"length":0': '"length":0.00'})
            .getResponse(ConfigureVideoResponse())
        )

    def configure(self, upload_id, photo, caption='', location=None, filter_=None):
        size = Image.open(photo).size[0]
        if caption is None:
            caption = ''

        requestData = (
            self.request('media/configure/')
            .addPost('_csrftoken', self.token)
            .addPost('media_folder', 'Instagram')
            .addPost('source_type', 4)
            .addPost('_uid', self.username_id)
            .addPost('_uuid', self.uuid)
            .addPost('caption', caption)
            .addPost('upload_id', upload_id)
            .addPost('device', OrderedDict([
                ('manufacturer',     self.settings.get('manufacturer')),
                ('model',            self.settings.get('model')),
                ('android_version',  Constants.ANDROID_VERSION),
                ('android_release',  Constants.ANDROID_RELEASE)
            ]))
            .addPost('edits', OrderedDict([
                ('crop_original_size',  [size, size]),
                ('crop_center',         [0, 0]),
                ('crop_zoom',           1)
            ]))
            .addPost('extra', OrderedDict([
                ('source_width',   size),
                ('source_height',  size)
            ]))
        )

        if location is not None:
            loc = OrderedDict([
                (location.getExternalIdSource() +'_id',     location.getExternalId()),
                ('name',                                    location.getName()),
                ('lat',                                     location.getLat()),
                ('lng',                                     location.getLng()),
                ('address',                                 location.getAddress()),
                ('external_source',                         location.getExternalIdSource())
            ])

            (requestData.addPost('location', json.dumps(loc))
             .addPost('geotag_enabled', true)
             .addPost('media_latitude', location.getLat())
             .addPost('posting_latitude', location.getLat())
             .addPost('media_longitude', location.getLng())
             .addPost('posting_longitude', location.getLng())
             .addPost('altitude', random.rand_int(10, 800)))

        if filter_ is not None:
            requestData.addPost('edits', {'filter_type': Utils.getFilterCode(filter_)})

        return (
            requestData.setReplacePost(OrderedDict([
                '"crop_center":[0,0]',                    '"crop_center":[0.0,-0.0]',
                '"crop_zoom":1' ,                         '"crop_zoom":1.0',
                '"crop_original_size":'+"["+str(size)+","+str(size)+"]",  '"crop_original_size":'+"["+str(size)+".0,"+str(size)+".0]"
            ]))
            .getResponse(ConfigureResponse())
        )

    def configureToReel(self, upload_id, photo):
        size = Image.open(photo).size[0]

        return (
            self.request('media/configure_to_reel/')
            .addPost('upload_id', upload_id)
            .addPost('source_type', 3)
            .addPost('edits', OrderedDict([
                'crop_original_size',  [size, size],
                'crop_zoom',           1.3333334,
                'crop_center',         [0.0, 0.0]
            ]))
            .addPost('extra', OrderedDict([
                'source_width',   size,
                'source_height',  size
            ]))
            .addPost('device', OrderedDict([
                'manufacturer',     self.settings.get('manufacturer'),
                'model',            self.settings.get('model'),
                'android_version',  Constants.ANDROID_VERSION,
                'android_release',  Constants.ANDROID_RELEASE
            ]))
            .addPost('_csrftoken', self.token)
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .setReplacePost({
                '"crop_center":[0,0]', '"crop_center":[0.0,0.0]'
            })
            .getResponse(ConfigureResponse())
        )

    def editMedia(self, mediaId, captionText='', usertags=None):
        """
        Edit media.
        :type mediaId: str
        :param mediaId: Media id
        :type captionText: str
        :param captionText: Caption text
        :rtype: object
        :return: edit media data
        """
        if usertags is None:
            return (
                self.request("media/" + mediaId + "/edit_media/")
                .addPost('_uuid', self.uuid)
                .addPost('_uid', self.username_id)
                .addPost('_csrftoken', self.token)
                .addPost('caption_text', captionText)
                .getResponse(EditMediaResponse())
            )
        else:
            return (
                self.request("media/" + mediaId + "/edit_media/")
                .addPost('_uuid', self.uuid)
                .addPost('_uid', self.username_id)
                .addPost('_csrftoken', self.token)
                .addPost('caption_text', captionText)
                .addPost('usertags', usertags)
                .getResponse(EditMediaResponse())
            )

    def removeSelftag(self, mediaId):
        """
        Remove yourself from a tagged media.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: edit media data
        """
        return (
            self.request("usertags/ " + mediaId + "/remove/")
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .getResponse(MediaResponse()) # FIXME MediaResponse is currently non-existant in PHP
        )

    def mediaInfo(self, mediaId):
        """
        Media info
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: delete request data
        """
        return (
            self.request("media/" + mediaId + "/info/")
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .addPost('media_id', mediaId)
            .getResponse(MediaInfoResponse())
        )

    def deleteMedia(self, mediaId):
        """
        Delete photo or video.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: delete request data
        """
        return (
            self.request("media/" + mediaId + "/delete/")
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .addPost('media_id', mediaId)
            .getResponse(MediaDeleteResponse())
        )

    def comment(self, mediaId, commentText):
        """
        Comment media.
        :type mediaId: str
        :param mediaId: Media id
        :type commentText: str
        :param commentText: Comment Text
        :rtype: object
        :return: comment media data
        """
        return (
            self.request("media/" + mediaId + "/comment/")
            .addPost('user_breadcrumb', Utils.generateUserBreadcrumb(len(commentText)))
            .addPost('idempotence_token', SignatureUtils.generateUUID(True))
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .addPost('comment_text', commentText)
            .addPost('containermodule', 'comments_feed_timeline')
            .getResponse(CommentResponse())
        )

    def deleteComment(self, mediaId, commentId):
        """
        Delete Comment.
        :type mediaId: str
        :param mediaId: Media ID
        :type commentId: str
        :param commentId: Comment ID
        :rtype: object
        :return: Delete comment data
        """
        return (
            self.request("media/" + mediaId + "/comment/" + commentId + "/delete/")
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .getResponse(DeleteCommentResponse())
        )

    def deleteCommentsBulk(self, mediaId, commentIds):
        """
        Delete Comment Bulk.

        :type mediaId: str
        :param mediaId: Media ID
        :type commentIds: list
        :param commentIds: List of comments to delete
        :rtype: object
        :return: Delete Comment Bulk Data
        """
        if not isinstance(commentIds, list):
            commentIds = [commentIds]

        string = []
        for commentId in commentIds:
            string.append(str(commentId))

        comment_ids_to_delete = ','.join(string)

        return (
            self.request("media/" + mediaId + "/comment/bulk_delete/")
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .addPost('comment_ids_to_delete', comment_ids_to_delete)
            .getResponse(DeleteCommentResponse())
        )

    def changeProfilePicture(self, photo):
        """
        Sets account to public.
        :type photo: str
        :param photo: Path to photo
        """

        # FIXME This doesn't make sense.
        # While this might be legal in PHP, this is illegal in python
        #return ProfileResponse(self.http.changeProfilePicture(photo))

        return self.http.changeProfilePicture(photo)

    def removeProfilePicture(self):
        """
        Remove profile picture.
        :rtype: object
        :return: status request data
        """
        return (
            self.request('accounts/remove_profile_picture/')
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .getResponse(ProfileResponse())
        )

    def setPrivateAccount(self):
        """
        Sets account to private.

        :rtype: object
        :return: status request data
        """
        return (
            self.request('accounts/set_private/')
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .getResponse(ProfileResponse())
        )

    def setPublicAccount(self):
        """
        Sets account to public.
        :rtype: object
        :return: status request data
        """
        return (
            self.request('accounts/set_public/')
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .getResponse(ProfileResponse())
        )

    def getProfileData(self):
        """
        Get personal profile data.
        :rtype: object
        :return:
        """
        return (
            self.request('accounts/current_user/')
            .addParams('edit', true)
            .addPost('_uuid', self.uuid)
            .addPost('_uid', self.username_id)
            .addPost('_csrftoken', self.token)
            .getResponse(ProfileResponse())
        )

    def editProfile(self, url, phone, first_name, biography, email, gender):
        """
        Edit profile.
        :type url: str
        :param url: Url - website. "" for nothing
        :type phone: str
        :param phone: Phone number. "" for nothing
        :type first_name: str
        :param first_name: Name. "" for nothing
        :type email: str
        :param email: Email. Required.
        :type gender: int
        :param gender: Gender. male = 1 , female = 0
        :rtype: object
        :return: edit profile data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('external_url', url),
                ('phone_number', phone),
                ('username', self.username),
                ('first_name', first_name),
                ('biography', biography),
                ('email', email),
                ('gender', gender)
            ])
        )

        return ProfileResponse(self.request('accounts/edit_profile/', SignatureUtils.generateSignature(data))[1])

    def changePassword(self, oldPassword, newPassword):
        """
        Change Password.

        :type oldPassword: str
        :param oldPassword: Old Password
        :type newPassword: str
        :param newPassword: New Password
        :rtype: object
        :return: Change Password Data
        """

        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('old_password', oldPassword),
                ('new_password1', newPassword),
                ('new_password2', newPassword)
            ])
        )
        return self.request('accounts/change_password/', SignatureUtils.generateSignature(data))[1]

    def getUsernameInfo(self, usernameId):
        """
        Get username info.
        :param usernameId: Username id
        :rtype: object
        :return: Username data
        """
        return self.request("users/" + str(usernameId) + "/info").getResponse(UsernameInfoResponse())

    def getSelfUsernameInfo(self):
        """
        Get self username info.
        :rtype: object
        :return: Username data
        """
        return self.getUsernameInfo(self.username_id)

    def getRecentActivity(self):
        """
        Get recent activity.
        :rtype: object
        :return: Recent activity data
        """
        return self.request('news/inbox/').addParams('activity_module', 'all').getResponse(ActivityNewsResponse())

    def getFollowingRecentActivity(self, maxid=None):
        """
        Get recent activity from accounts followed.

        :rtype: object
        :return: Recent activity data of follows
        """

        activity = self.request('news/')
        if maxid is not None:
            activity.addParams('max_id', maxid)

        return activity.getResponse(FollowingRecentActivityResponse())

    def getv2Inbox(self):
        """
        I dont know this yet.
        :rtype: object
        :return: v2 inbox data
        """
        return self.request('direct_v2/inbox/?').getResponse(V2InboxResponse())

    def getUserTags(self, usernameId, maxid=None, minTimestamp=None):
        """
        Get user tags.
        :type usernameId: str
        :param usernameId:
        :rtype: object
        :return: user tags data
        """
        return (
            self.request("usertags/$usernameId/feed/")
            .addParams('rank_token', self.rank_token)
            .addParams('ranked_content', 'true')
            .addParams('max_id', maxid if maxid is not None else '')
            .addParams('min_timestamp', minTimestamp if minTimestamp is not None else '')
            .getResponse(UsertagsResponse())
        )

    def getSelfUserTags(self):
        """
        Get self user tags.
        :rtype: object
        :return: self user tags data
        """
        return self.getUserTags(self.username_id)

    def getMediaLikers(self, mediaId):
        """
        Get media likers.
        :type mediaId: str
        :param mediaId:
        :rtype: object
        :return:
        """
        return self.request("media/" + mediaId + "/likers/").getResponse(MediaLikersResponse())

    def getGeoMedia(self, usernameId):
        """
        Get user locations media.
        :type usernameId: str
        :param usernameId: Username id
        :rtype: object
        :return: Geo Media data
        """
        return self.request("maps/user/" + str(usernameId)).getResponse(GeoMediaResponse())

    def getSelfGeoMedia(self):
        """
        Get self user locations media.
        :rtype: object
        :return: Geo Media data
        """
        return self.getGeoMedia(self.username_id)

    def searchLocation(self, latitude, longitude, query=None):
        locations = (
            self.request('location_search/')
            .addParams('rank_token', self.rank_token)
            .addParams('latitude', latitude)
            .addParams('longitude', longitude)
        )

        if query is None:
            locations.addParams('timestamp', int(time.time()))
        else:
            locations.addParams('search_query', query)

        return locations.getResponse(LocationResponse())

    def fbUserSearch(self, query):
        """
        facebook user search.
        :type query: str
        :param query:
        :rtype: object
        :return: query data
        """
        query = urllib.quote(query)

        return (
            self.request('fbsearch/topsearch/')
            .addParams('context', 'blended')
            .addParams('query', query)
            .addParams('rank_token', self.rank_token)
            .getResponse(FBSearchResponse())
        )

    def searchUsers(self, query):
        """
        Search users.
        :type query: str
        :param query:
        :rtype: object
        :return: query data
        """
        return (
            self.request('users/search/')
            .addParams('ig_sig_key_version', Constants.SIG_KEY_VERSION)
            .addParams('is_typeahead', True)
            .addParams('query', query)
            .addParams('rank_token', self.rank_token)
            .getResponse(SearchUserResponse())
        )

    def searchUsername(self, usernameName):
        """
        Search exact username

        :type usernameName: str
        :param usernameName: username as STRING not an id

        :rtype: object
        :return: query data
        """
        return self.request("users/" + usernameName + "/usernameinfo").getResponse(UsernameInfoResponse())

    def getUsernameId(self, username):
        return self.searchUsername(username).getUser().getPk()

    def syncFromAdressBook(self, contacts):
        """
        Search users using addres book.
        :type contacts: list
        :param contacts:
        :rtype: object
        :return:
        """
        data = OrderedDict([(
            ('contacts=', json.dumps(contacts))
        )])
        return self.request('address_book/link/?include=extra_display_name,thumbnails', data)[1]

    def searchTags(self, query):
        """
        Search tags.
        :type query: str
        :param query:
        :rtype: object
        :return: query data
        """
        query = self.request("tags/search/?is_typeahead=true&q=" + query + "&rank_token=" + self.rank_token)[1]

        if query['status'] != 'ok':
            raise InstagramException(query['message'] + "\n")

        return query

    def getTimeline(self, maxid=None):
        """
        Get timeline data.
        :rtype: object
        :return: timeline data
        """
        timeline = self.request(
            "feed/timeline/?rank_token=" + self.rank_token + "&ranked_content=true" +
            (("&max_id=" + str(maxid)) if maxid is not None else '')
        )[1]

        if timeline['status'] != 'ok':
            raise InstagramException(timeline['message'] + "\n")

        return timeline

    def getReelsTrayFeed(self):
        return self.request('feed/reels_tray/').getResponse(ReelsTrayFeedResponse())

    def getUserFeed(self, usernameId, maxid=None, minTimestamp=None):
        """
        Get user feed.
        :type usernameId: str
        :param usernameId: Username id
        :type maxid: str
        :param maxid: Max Id
        :type minTimestamp: str
        :param minTimestamp: Min timestamp
        :rtype: object
        :return: User feed data
        :raises: InstagramException
        """
        return (
            self.request("feed/user/" + str(usernameId) + "/")
            .addParams('rank_token', self.rank_token)
            .addParams('ranked_content', 'true')
            .addParams('max_id', str(maxid) if maxid is not None else '')
            .addParams('min_timestamp', str(minTimestamp) if minTimestamp is not None else '')
            .getResponse(UserFeedResponse())
        )

    def getHashtagFeed(self, hashtagString, maxid=''):
        """
        Get hashtag feed.
        :type hashtagString: str
        :param hashtagString: Hashtag string, not including the #
        :rtype: object
        :return: Hashtag feed data
        """
        if maxid == '':
            endpoint = "feed/tag/" + hashtagString + "/?rank_token=" + self.rank_token + "&ranked_content=true&"
        else:
            endpoint = "feed/tag/" + hashtagString + "/?max_id=" \
                       + maxid + "&rank_token=" + self.rank_token + "&ranked_content=true&"
        hashtagFeed = self.request(endpoint)[1]
        if hashtagFeed['status'] != 'ok':
            raise InstagramException(hashtagFeed['message'] + "\n")

        return hashtagFeed

    def searchFBLocation(self, query):
        """
        Get locations.
        :type query: str
        :param query: search query
        :rtype: object
        :return: Location location data
        """
        query = urllib.quote(query)
        endpoint = "fbsearch/places/?rank_token=" + self.rank_token + "&query=" + query

        locationFeed = self.request(endpoint)[1]

        if locationFeed['status'] != 'ok':
            raise InstagramException(locationFeed['message'] + "\n")

        return locationFeed

    def getLocationFeed(self, locationId, maxid=''):
        """
        Get location feed.
        :type locationId: str
        :param locationId: location id
        :rtype: object
        :return: Location feed data
        """
        if maxid is '':
            endpoint = "feed/location/" + locationId + "/?rank_token=" + self.rank_token + "&ranked_content=true&"
        else:
            endpoint = "feed/location/" + locationId + "/?max_id=" \
                       + maxid + "&rank_token=" + self.rank_token + "&ranked_content=true&"

        locationFeed = self.request(endpoint)[1]

        if locationFeed['status'] != 'ok':
            raise InstagramException(locationFeed['message'] + "\n")

        return locationFeed

    def getSelfUserFeed(self, max_id=None):
        """
        Get self user feed.
        :rtype: object
        :return: User feed data
        """
        return self.getUserFeed(self.username_id, max_id)

    def getPopularFeed(self):
        """
        Get popular feed.
        :rtype: object
        :return: popular feed data
        """
        popularFeed = self.request("feed/popular/?people_teaser_supported=1&rank_token=" \
                                        + self.rank_token + "&ranked_content=true&")[1]

        if popularFeed['status'] != 'ok':
            raise InstagramException(popularFeed['message'] + "\n")

        return popularFeed

    def getUserFollowings(self, usernameId, maxid=''):
        """
        Get user followings.
        :type usernameId: str
        :param usernameId: Username id

        :rtype: object
        :return: followers data
        """
        return FollowingResponse(self.request(
            "friendships/" + usernameId + "/following/?max_id=" + maxid + "&ig_sig_key_version="
            + Constants.SIG_KEY_VERSION + "&rank_token=" + self.rank_token)[1])

    def getUserFollowers(self, usernameId, maxid=''):
        """
        Get user followers.
        :type usernameId: str
        :param usernameId: Username id

        :rtype: object
        :return: followers data
        """
        return FollowerResponse(self.request(
            "friendships/" + usernameId + "/followers/?max_id=" + maxid
            + "&ig_sig_key_version=" + Constants.SIG_KEY_VERSION + "&rank_token=" + self.rank_token)[1])

    def getSelfUserFollowers(self):
        """
        Get self user followers.

        :rtype: object
        :return: followers data
        """
        return self.getUserFollowers(self.username_id)

    def getSelfUsersFollowing(self):
        """
        Get self users we are following.

        :rtype: object
        :return: users we are following data
        """
        return self.getUserFollowings(self.username_id)

    def like(self, mediaId):
        """
        Like photo or video.

        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: status request
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('media_id', mediaId)
            ])
        )
        return self.request("media/" + mediaId + "/like/", SignatureUtils.generateSignature(data))[1]

    def unlike(self, mediaId):
        """
        Unlike photo or video.

        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: status request
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('media_id', mediaId)
            ])
        )
        return self.request("media/" + mediaId + "/unlike/", SignatureUtils.generateSignature(data))[1]

    def getMediaComments(self, mediaId, maxid=''):
        """
        Get media comments.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: Media comments data
        """
        return MediaCommentsResponse(self.request("media/" + str(mediaId) + "/comments/?max_id=" + str(maxid)
                                                       + "&ig_sig_key_version=" + Constants.SIG_KEY_VERSION)[1])

    def setNameAndPhone(self, name='', phone=''):
        """
        Set name and phone (Optional).
        :type name: str
        :param name:
        :type phone: str
        :param phone:
        :rtype: object
        :return: Set status data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('first_name', name),
                ('phone_number', phone),
                ('_csrftoken', self.token)
            ])
        )

        return self.request("accounts/set_phone_and_name/", SignatureUtils.generateSignature(data))[1]

    def getDirectShare(self):
        """
        Get direct share.

        :rtype: object
        :return: Direct share data
        """
        return self.request('direct_share/inbox/?')[1]

    def backup(self):
        """
        Backups all your uploaded photos :).
        """
        go = False
        while True:
            if not go:
                myUploads = self.getSelfUserFeed()
            else:
                myUploads = self.getSelfUserFeed(myUploads.getNextMaxId() if myUploads.getNextMaxId() else None)
                # fixme local variable `myUploads` might be referenced before assignment
            if not os.path.isdir(self.IGDataPath + 'backup/'):
                os.mkdir(self.IGDataPath + 'backup/')

            for item in myUploads.getItems():
                dir_name = self.IGDataPath + 'backup/' + self.username + "-" + time.strftime('%Y-%m-%d')
                if not os.path.isdir(dir_name):
                    os.mkdir(dir_name)

                if item.getVideoVersions():
                    file_put_contents(
                        os.path.join(dir_name, item.getMediaId() + '.mp4'),
                        urllib.urlopen(item.getVideoVersions()[0].getUrl()).read()
                    )  # todo test and remove below
                else:
                    file_put_contents(
                        os.path.join(dir_name, item.getMediaId() + '.jpg'),
                        urllib.urlopen(item.getImageVersions()[0].getUrl()).read()
                    )  # todo test and remove below

                    # urllib.urlretrieve(
                    #    item['image_versions2']['candidates'][0]['url'],
                    #    self.IGDataPath + 'backup/' + self.username + "-" + time.strftime('%Y-%m-%d') + '/' + item['id'] + '.jpg'
                    # )
            go = True
            if not myUploads.getNextMaxId():
                break

    def follow(self, userId):
        """
        Follow.

        :param userId:
        :type userId: str
        :rtype: object
        :return: Friendship status data
        """

        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('user_id', userId),
                ('_csrftoken', self.token)

            ])
        )

        return self.request("friendships/create/" + userId + "/", SignatureUtils.generateSignature(data))[1]

    def unfollow(self, userId):
        """
        Unfollow.

        :param userId:
        :type userId: str
        :rtype: object
        :return: Friendship status data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('user_id', userId),
                ('_csrftoken', self.token)
            ])
        )

        return self.request("friendships/destroy/" + userId + "/", SignatureUtils.generateSignature(data))[1]

    def block(self, userId):
        """
        Block.

        :param userId:
        :type userId: str
        :rtype: object
        :return: Friendship status data
        """

        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('user_id', userId),
                ('_csrftoken', self.token)
            ])
        )

        return self.request("friendships/block/" + userId + "/", SignatureUtils.generateSignature(data))[1]

    def unblock(self, userId):
        """
        Unblock.

        :param userId:
        :type userId: str
        :rtype: object
        :return: Friendship status data
        """

        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('user_id', userId),
                ('_csrftoken', self.token)
            ])
        )

        return self.request("friendships/unblock/" + userId + "/", SignatureUtils.generateSignature(data))[1]

    def userFriendship(self, userId):
        """
        Show User Friendship.

        :type userId: str
        :param userId:
        :rtype: object
        :return: Friendship relationship data
        """

        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('user_id', userId),
                ('_csrftoken', self.token)
            ])
        )

        return self.request("friendships/show/" + userId + "/", SignatureUtils.generateSignature(data))[1]

    def getLikedMedia(self, maxid=None):
        """
        Get liked media.

        :rtype: object
        :return: Liked media data
        """
        endpoint = 'feed/liked/?' + (('max_id=' + str(maxid) + '&') if maxid is not None else '')
        return self.request(endpoint)[1]

    def verifyPeer(self, enable):
        self.http.verifyPeer(enable)

    def verifyHost(self, enable):
        self.http.verifyHost(enable)

    def request(self, url):
        return Request(url)

    @staticmethod
    def getInstance():
        if Instagram.instance == None:
            Instagram.instance = Instagram()

        return Instagram.instance


class Request:
    def __init__(self, url):
        self.params = OrderedDict()
        self.posts = OrderedDict()
        self.requireLogin_ = False
        self.floodWait = False
        self.checkStatus = True
        self.signedPost = True
        self.replacePost = {}

        self.url = url

    def addParams(self, key, value):
        if value == True:
            value = "true"

        self.params[key] = value

        return self

    def addPost(self, key, value):
        self.posts[key] = value

        return self

    def requireLogin(self, requireLogin_=False):
        self.requireLogin_ = requireLogin_

        return self

    def setFloodWait(self, floodWait=False):
        self.floodWait = floodWait

        return self

    def setCheckStatus(self, checkStatus=True):
        self.checkStatus = checkStatus

        return self

    def setSignedPost(self, signedPost=True):
        self.signedPost = signedPost

        return self

    def setReplacePost(self, replace=[]):
        self.replacePost = replace

        return self

    def getResponse(self, obj, includeHeader = False):
        instagramObj = Instagram.getInstance()

        if self.params:
            endPoint = self.url + "?" + compat_urllib_parse.urlencode(self.params)
        else:
            endPoint = self.url
        if self.posts:
            if self.signedPost:
                post = SignatureUtils.generateSignature(json.dumps(self.posts))
            else:
                post = compat_urllib_parse.urlencode(self.posts)
        else:
            post = None
        if self.replacePost:
            for key in self.replacePost:
                post = post.replace(key, self.replacePost[key])

        response = instagramObj.http.request(endPoint, post, self.requireLogin_, self.floodWait, False)

        if response[1] == None:
            raise InstagramException('No response from server, connection or configure error', ErrorCode.EMPTY_RESPONSE)

        # Here we deviate from the PHP function because JsonMapper doesn't exist for python AFAIK
        def _map(obj, root):
            if root is None:
                obj = None
                return
            if type(root) in [str, int, float]:
                obj = root
                return
            if type(root) is list:
                keys = list(obj.__dict__.keys())
                for i in range(len(root)):
                    obj.__dict__[keys[i]] = root[i]
                return
            for key in root:
                if "_types" in obj.__dict__ and key in obj._types:
                    if type(obj._types[key]) is list:
                        obj.__dict__[key] = []
                        # TODO: check if root[key] is list
                        for i in range(len(root[key])):
                            obj.__dict__[key].append(obj._types[key][0]())
                            _map(obj.__dict__[key][i], root[key][i])
                    else:
                        obj.__dict__[key] = obj._types[key]()
                        _map(obj.__dict__[key], root[key])
                else:
                    obj.__dict__[key] = root[key]
        _map(obj, response[1])
        responseObject = obj

        if self.checkStatus and not responseObject.isOk():
            raise InstagramException(obj.__class__.__name__ + ' : ' + responseObject.getMessage())

        if includeHeader:
            responseObject.setFullResponse(response)
        else:
            responseObject.setFullResponse(response[1])

        return responseObject

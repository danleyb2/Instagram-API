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
    def __init__(self, username, password, debug=False, IGDataPath=None, truncatedDebug=False):

        """
        Default class constructor.
        :type username: str
        :param username: Your Instagram username.
        :type password: str
        :param password: Your Instagram password.
        :param debug: Debug on or off, False by default.
        :param IGDataPath: Default folder to store data, you can change it.
        """
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
        self.device_id = SignatureUtils.generateDeviceId(hashlib.md5((username + password).encode("utf-8")))

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
                os.mkdir(self.IGDataPath, 0777)

        self.checkSettings(username)

        self.http = HttpInterface(self)

        self.setUser(username, password)


    def getUserLive(self):
        """
        https://i.instagram.com/api/v1/live/
        Get user reels.
        :return: User feed data
        :raises: InstagramException
        """
        # //feed/reels_tray/https://i.instagram.com/api/v1/

        userFeed = self.http.request("feed/reels_tray/")[1]

        # ;
        # "feed/live/")[1]
        # "feed/user/"+str(usernameId)+"/reel_media/"
        # + str(usernameId) + "/live/?rank_token=" + self.rank_token)[1]

        if userFeed['status'] != 'ok':
            raise InstagramException(userFeed['message'] + "\n")

        return userFeed

        #   Evil Funct

    def getUserStory(self, usernameId):
        """

        Get user story.
        :type usernameId: str
        :param usernameId: Username id
        :return: User feed data
        :raises: InstagramException
        """
        userFeed = self.http.request("feed/user/" + str(usernameId) + "/story/?rank_token=" + self.rank_token)[1]

        if userFeed['status'] != 'ok':
            raise InstagramException(userFeed['message'] + "\n")

        return userFeed

    def setUser(self, username, password):
        """
         Set the user. Manage multiple accounts.

        :type username: str
        :param username: Your Instagram username.
        :type password: str
        :param password: Your Instagram password.
        :
        """
        self.username = username
        self.password = password

        self.checkSettings(username)

        self.uuid = SignatureUtils.generateUUID(True)

        if os.path.isfile(self.IGDataPath + self.username + '-cookies.dat') and \
                (self.settings.get('username_id') != None) and \
                (self.settings.get('token') != None):
            self.isLoggedIn = True
            self.username_id = self.settings.get('username_id')
            self.rank_token = self.username_id + '_' + self.uuid
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
            fetch = self.http.request(
                'si/fetch_headers/?challenge_type=signup&guid=' + SignatureUtils.generateUUID(False), None, True)
            header = fetch[0]
            response = ChallengeResponse(fetch[1])

            if not header or not response.isOk():
                raise InstagramException("Couldn't get challenge, check your connection")
                # return response #FIXME unreachable code

            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', fetch[0], re.MULTILINE)
            if match:
                self.token = match.group(1)
            else:
                raise InstagramException('Missing csfrtoken')

            data = OrderedDict([
                ('username', self.username),
                ('guid', self.uuid),
                ('device_id', self.device_id),
                ('password', self.password),
                ('login_attempt_count', 0)
            ])

            login = self.http.request('accounts/login/', SignatureUtils.generateSignature(json.dumps(data)), True)
            response = LoginResponse(login[1])

            if not response.isOk(): raise InstagramException(response.getMessage())

            self.isLoggedIn = True
            self.username_id = response.getUsernameId()
            self.settings.set('username_id', self.username_id)
            self.rank_token = self.username_id + '_' + self.uuid
            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', login[0], re.MULTILINE)
            if match: self.token = match.group(1)
            self.settings.set('token', self.token)

            self.syncFeatures()
            self.autoCompleteUserList()
            self.timelineFeed()
            self.getRankedRecipients()
            self.getRecentRecipients()
            self.megaphoneLog()
            self.getv2Inbox()
            self.getRecentActivity()
            self.getReelsTrayFeed()
            self.explore()

            return response

        check = self.timelineFeed()

        if check.getMessage() == 'login_required':
            self.login(True)

        self.autoCompleteUserList()
        self.getReelsTrayFeed()
        self.getRankedRecipients()
        # push register
        self.getRecentRecipients()
        # push register
        self.megaphoneLog()
        self.getv2Inbox()
        self.getRecentActivity()
        self.explore()

    def syncFeatures(self, prelogin=False):
        if prelogin:
            data = json.dumps(
                OrderedDict([
                    ('id', SignatureUtils.generateUUID(True)),
                    ('experiments', Constants.LOGIN_EXPERIMENTS)
                ])
            )
            return SyncResponse(self.http.request('qe/sync/', SignatureUtils.generateSignature(data), True)[1])
        else:

            data = json.dumps(
                OrderedDict([
                    ('_uuid', self.uuid),
                    ('_uid', self.username_id),
                    ('_csrftoken', self.token),
                    ('id', self.username_id),
                    ('experiments', Constants.EXPERIMENTS)
                ])
            )
            return SyncResponse(self.http.request('qe/sync/', SignatureUtils.generateSignature(data))[1])

    def autoCompleteUserList(self):
        return autoCompleteUserListResponse(self.http.request('friendships/autocomplete_user_list/?version=2')[1])

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

    def timelineFeed(self):
        return TimelineFeedResponse(self.http.request('feed/timeline/')[1])

    def megaphoneLog(self):
        data = OrderedDict([
                ('type', 'feed_aysf'),
                ('action', 'seen'),
                ('reason', ''),
                ('_uuid', self.uuid),
                ('device_id', self.device_id),
                ('_csrftoken', self.token),
                ('uuid', hashlib.md5(str(int(time.time())).encode("utf-8")).hexdigest())
        ])

        return MegaphoneLogResponse(self.http.request('megaphone/log/', compat_urllib_parse.urlencode(data))[1])

    def getPendingInbox(self):
        """
        Pending Inbox

        :rtype: object
        :return: Pending Inbox Data
        """
        pendingInbox = PendingInboxResponse(self.http.request('direct_v2/pending_inbox/?')[1])

        if not pendingInbox.isOk():
            raise InstagramException(pendingInbox.getMessage() + "\n")
            # return FIXME unreachable code

        return pendingInbox

    def getRankedRecipients(self):
        """
        Ranked recipients.

        :rtype:list
        :return: Ranked recipients Data
        """
        print self.http.request('direct_v2/ranked_recipients/?show_threads=true')

        ranked_recipients = RankedRecipientsResponse(
            self.http.request('direct_v2/ranked_recipients/?show_threads=true')[1]
        )

        if not ranked_recipients.isOk():
            raise InstagramException(ranked_recipients.getMessage() + "\n")
            # return todo unreachable code

        return ranked_recipients

    def getRecentRecipients(self):
        """
        Recent recipients.

        :rtype: list
        :return: Ranked recipients Data
        """
        recent_recipients = RecentRecipientsResponse(self.http.request('direct_share/recent_recipients/')[1])

        if not recent_recipients.isOk():
            raise InstagramException(recent_recipients.getMessage() + "\n")
            # return todo unreachable code

        return recent_recipients

    def explore(self):
        """
        Explore Tab

        :rtype: object
        :return: Explore data
        """
        explore = ExploreResponse(self.http.request('discover/explore/')[1])

        if not explore.isOk():
            raise InstagramException(explore.getMessage() + "\n")

            # return todo unreachable code
        return explore

    def expose(self):
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('id', self.username_id),
                ('_csrftoken', self.token),
                ('experiment', 'ig_android_profile_contextual_feed')
            ])
        )
        return ExposeResponse(self.http.request('qe/expose/', SignatureUtils.generateSignature(data))[1])

    def logout(self):
        """
        Logout of Instagram.

        :rtype: bool
        :return: Returns true if logged out correctly
        """
        logout = LogoutResponse(self.http.request('accounts/logout/')[1])

        if logout.isOk():
            return True
        else:
            return False

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
        return self.http.uploadVideo(video, caption), customPreview

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
        return self.http.request(
            "direct_v2/threads/" + str(threadId) + "/" + str(threadAction) + "/",
            self.generateSignature(data)  # todo Unresolved reference
        )[1]

    def configureVideo(self, upload_id, video, caption='', customPreview=None):

        self.uploadPhoto(video, caption, upload_id, customPreview)
        size = Image.open(video).size[0]

        post = json.dumps(
            OrderedDict([
                ('upload_id', upload_id),
                ('source_type', 3),
                ('poster_frame_index', 0),
                ('length', 0.00),
                ('audio_muted', False),
                ('filter_type', '0'),
                ('video_result', 'deprecated'),
                ('clips', OrderedDict([
                    ('length', Utils.getSeconds(video)),
                    ('source_type', '3'),
                    ('camera_position', 'back')
                ])),
                ('extra', OrderedDict([
                    ('source_width', 960),
                    ('source_height', 1280)
                ])),

                ('device', OrderedDict([
                    ('manufacturer', self.settings.get('manufacturer')),
                    ('model', self.settings.get('model')),
                    ('android_version', Constants.ANDROID_VERSION),
                    ('android_release', Constants.ANDROID_RELEASE)
                ])),
                ('_csrftoken', self.token),
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('caption', caption)

            ])

        )

        post = post.replace('"length":0', '"length":0.00')

        return ConfigureVideoResponse(
            self.http.request('media/configure/?video=1', SignatureUtils.generateSignature(post))[1])

    def configure(self, upload_id, photo, caption='', location=None, filter_=None):
        caption = caption if caption else ''
        size = Image.open(photo).size[0]

        post = OrderedDict([
                ('upload_id', upload_id),
                ('camera_model', self.settings.get('model').replace(" ", "")),
                ('source_type', 3),
                ('date_time_original', time.strftime('%Y:%m:%d %H:%M:%S')),
                ('camera_make', self.settings.get('manufacturer')),
                ('edits', OrderedDict([
                    ('crop_original_size', [size, size]),
                    ('crop_zoom', 1.3333334),
                    ('crop_center', [0.0, -0.0])
                ])),
                ('extra', OrderedDict([
                    ('source_width', size),
                    ('source_height', size)
                ])),

                ('device', OrderedDict([
                    ('manufacturer', self.settings.get('manufacturer')),
                    ('model', self.settings.get('model')),
                    ('android_version', Constants.ANDROID_VERSION),
                    ('android_release', Constants.ANDROID_RELEASE)
                ])),
                ('_csrftoken', self.token),
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('caption', caption)

        ])
        if location:
            loc = OrderedDict([
                (str(location.getExternalIdSource()) + '_id', location.getExternalId()),
                ('name', location.getName()),
                ('lat', location.getLatitude()),
                ('lng', location.getLongitude()),
                ('address', location.getAddress()),
                ('external_source', location.getExternalIdSource())
            ])
            post['location'] = json.dumps(loc)
            post['geotag_enabled'] = True
            post['media_latitude'] = location.getLatitude()
            post['posting_latitude'] = location.getLatitude()
            post['media_longitude'] = location.getLongitude()
            post['posting_longitude'] = location.getLongitude()
            post['altitude'] = mt_rand(10, 800)

        if filter_:
            post['edits']['filter_type'] = Utils.getFilterCode(filter)

        post = json.dumps(post)
        post = post.replace('"crop_center":[0,0]', '"crop_center":[0.0,-0.0]')

        return ConfigureResponse(self.http.request('media/configure/', SignatureUtils.generateSignature(post))[1])

    def configureToReel(self, upload_id, photo):

        size = Image.open(photo).size[0]

        post = json.dumps(
            OrderedDict([
                ('upload_id', upload_id),
                ('source_type', 3),
                ('edits', OrderedDict([
                    ('crop_original_size', [size, size]),
                    ('crop_zoom', 1.3333334),
                    ('crop_center', [0.0, 0.0])
                ])),
                ('extra', OrderedDict([
                    ('source_width', size),
                    ('source_height', size)
                ])),

                ('device', OrderedDict([
                    ('manufacturer', self.settings.get('manufacturer')),
                    ('model', self.settings.get('model')),
                    ('android_version', Constants.ANDROID_VERSION),
                    ('android_release', Constants.ANDROID_RELEASE)
                ])),
                ('_csrftoken', self.token),
                ('_uuid', self.uuid),
                ('_uid', self.username_id),

            ])
        )
        post = post.replace('"crop_center":[0,0]', '"crop_center":[0.0,0.0]')

        return ConfigureResponse(
            self.http.request('media/configure_to_reel/', SignatureUtils.generateSignature(post))[1])

    def editMedia(self, mediaId, captionText=''):
        """
        Edit media.
        :type mediaId: str
        :param mediaId: Media id
        :type captionText: str
        :param captionText: Caption text
        :rtype: object
        :return: edit media data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('caption_text', captionText)
            ])
        )
        # Unresolved Reference MediaResponse
        return MediaResponse(
            self.http.request("media/" + mediaId + "/edit_media/", SignatureUtils.generateSignature(data))[1]['media']
        )

    def removeSelftag(self, mediaId):
        """
        Remove yourself from a tagged media.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: edit media data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token)
            ])
        )

        # Unresolved Reference MediaResponse
        return MediaResponse(
            self.http.request("usertags/" + mediaId + "/remove/", SignatureUtils.generateSignature(data))[1]
        )

    def mediaInfo(self, mediaId):
        """
        Media info
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: delete request data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('media_id', mediaId)
            ])
        )
        return MediaInfoResponse(
            self.http.request("media/" + mediaId + "/info/", SignatureUtils.generateSignature(data))[1])

    def deleteMedia(self, mediaId):
        """
        Delete photo or video.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: delete request data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('media_id', mediaId)
            ])
        )
        return self.http.request("media/" + mediaId + "/delete/", SignatureUtils.generateSignature(data))[1]

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
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('comment_text', commentText)
            ])
        )
        return CommentResponse(
            self.http.request("media/" + mediaId + "/comment/", SignatureUtils.generateSignature(data))[1]
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
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token)
            ])
        )
        return \
            self.http.request("media/" + mediaId + "/comment/" + commentId + "/delete/",
                              SignatureUtils.generateSignature(data))[1]

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

        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token),
                ('comment_ids_to_delete', comment_ids_to_delete)
            ])
        )
        return self.http.request("media/" + mediaId + "/comment/bulk_delete/",
                                 SignatureUtils.generateSignature(data))[1]

    def changeProfilePicture(self, photo):
        """
        Sets account to public.
        :type photo: str
        :param photo: Path to photo
        """
        self.http.changeProfilePicture(photo)

    def removeProfilePicture(self):
        """
        Remove profile picture.
        :rtype: object
        :return: status request data
        """
        data = json.dumps(
            OrderedDict([('_uuid', self.uuid), ('_uid', self.username_id), ('_csrftoken', self.token)])
        )
        return self.http.request('accounts/remove_profile_picture/', SignatureUtils.generateSignature(data))[1]

    def setPrivateAccount(self):
        """
        Sets account to private.

        :rtype: object
        :return: status request data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token)
            ])
        )
        return self.http.request('accounts/set_private/', SignatureUtils.generateSignature(data))[1]

    def setPublicAccount(self):
        """
        Sets account to public.
        :rtype: object
        :return: status request data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token)
            ])
        )
        return self.http.request('accounts/set_public/', SignatureUtils.generateSignature(data))[1]

    def getProfileData(self):
        """
        Get personal profile data.
        :rtype: object
        :return:
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('_csrftoken', self.token)
            ])
        )
        return ProfileResponse(
            self.http.request('accounts/current_user/?edit=true', SignatureUtils.generateSignature(data))[1])

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

        return ProfileResponse(self.http.request('accounts/edit_profile/', SignatureUtils.generateSignature(data))[1])

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
        return self.http.request('accounts/change_password/', SignatureUtils.generateSignature(data))[1]

    def getUsernameInfo(self, usernameId):
        """
        Get username info.
        :param usernameId: Username id
        :rtype: object
        :return: Username data
        """
        return UsernameInfoResponse(self.http.request("users/" + str(usernameId) + "/info/")[1])

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
        activity = self.http.request('news/inbox/')[1]

        if activity['status'] != 'ok':
            raise InstagramException(activity['message'] + "\n")

        return activity

    def getFollowingRecentActivity(self):
        """
        Get recent activity from accounts followed.

        :rtype: object
        :return: Recent activity data of follows
        """
        activity = self.http.request('news/?')[1]
        if activity['status'] != 'ok':
            raise InstagramException(activity['message'] + "\n")

        return activity

    def getv2Inbox(self):
        """
        I dont know this yet.
        :rtype: object
        :return: v2 inbox data
        """
        inbox = V2InboxResponse(self.http.request('direct_v2/inbox/?')[1])

        if not inbox.isOk():
            raise InstagramException(inbox.getMessage() + "\n")

        return inbox

    def getUserTags(self, usernameId):
        """
        Get user tags.
        :type usernameId: str
        :param usernameId:
        :rtype: object
        :return: user tags data
        """
        tags = UsertagsResponse(self.http.request("usertags/" + str(usernameId) + "/feed/?rank_token=" + self.rank_token
                                                  + "&ranked_content=true&")[1])
        if not tags.isOk():
            raise InstagramException(tags.getMessage() + "\n")

        return tags

    def getSelfUserTags(self):
        """
        Get self user tags.
        :rtype: object
        :return: self user tags data
        """
        return self.getUserTags(self.username_id)

    def tagFeed(self, tag):
        """
        Get tagged media.
        :type tag: str
        :param tag:
        :rtype: object
        :return:
        """
        userFeed = TagFeedResponse(
            self.http.request("feed/tag/" + tag + "/?rank_token=" + self.rank_token + "&ranked_content=true&")[1])

        if not userFeed.isOk():
            raise InstagramException(userFeed.getMessage() + "\n")

        return userFeed

    def getMediaLikers(self, mediaId):
        """
        Get media likers.
        :type mediaId: str
        :param mediaId:
        :rtype: object
        :return:
        """
        likers = MediaLikersResponse(self.http.request("media/" + mediaId + "/likers/")[1])
        if not likers.isOk():
            raise InstagramException(likers.getMessage() + "\n")
            # return #fixme unreachable code

        return likers

    def getGeoMedia(self, usernameId):
        """
        Get user locations media.
        :type usernameId: str
        :param usernameId: Username id
        :rtype: object
        :return: Geo Media data
        """
        locations = self.http.request("maps/user/" + str(usernameId) + "/")[1]

        if locations['status'] != 'ok':
            raise InstagramException(locations['message'] + "\n")

        return locations

    def getSelfGeoMedia(self):
        """
        Get self user locations media.
        :rtype: object
        :return: Geo Media data
        """
        return self.getGeoMedia(self.username_id)

    def searchLocation(self, latitude, longitude, query=None):
        locationQuery = OrderedDict([
            ('rank_token', self.rank_token),
            ('latitude', latitude),
            ('longitude', longitude)
        ])

        if query:
            locationQuery['timestamp'] = int(time.time())
        else:
            locationQuery['search_query'] = query  # TODO possible bug, query is None

        locations = LocationResponse(self.http.request("location_search/?" + urllib.urlencode(locationQuery))[1])

        if not locations.isOk():
            raise InstagramException(locations.getMessage() + "\n")
            # return fixme unreachable code

        return locations

    def fbUserSearch(self, query):
        """
        facebook user search.
        :type query: str
        :param query:
        :rtype: object
        :return: query data
        """
        query = urllib.quote(query)
        query = \
            self.http.request("fbsearch/topsearch/?context=blended&query=" + query + "&rank_token=" + self.rank_token)[
                1]

        if query['status'] != 'ok':
            raise InstagramException(query['message'] + "\n")

        return query

    def searchUsers(self, query):
        """
        Search users.
        :type query: str
        :param query:
        :rtype: object
        :return: query data
        """
        query = self.http.request(
            'users/search/?ig_sig_key_version=' + Constants.SIG_KEY_VERSION \
            + "&is_typeahead=true&query=" + query + "&rank_token=" + self.rank_token)[1]

        if query['status'] != 'ok':
            raise InstagramException(query['message'] + "\n")

        return query

    def searchUsername(self, usernameName):
        """
        Search exact username

        :type usernameName: str
        :param usernameName: username as STRING not an id

        :rtype: object
        :return: query data
        """
        query = UsernameInfoResponse(self.http.request("users/" + usernameName + "/usernameinfo/")[1])

        if not query.isOk():
            raise InstagramException(query.getMessage() + "\n")

        return query

    def getUsernameId(self, username):
        return self.searchUsername(username).getUsernameId()

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
        return self.http.request('address_book/link/?include=extra_display_name,thumbnails', data)[1]

    def searchTags(self, query):
        """
        Search tags.
        :type query: str
        :param query:
        :rtype: object
        :return: query data
        """
        query = self.http.request("tags/search/?is_typeahead=true&q=" + query + "&rank_token=" + self.rank_token)[1]

        if query['status'] != 'ok':
            raise InstagramException(query['message'] + "\n")

        return query

    def getTimeline(self, maxid=None):
        """
        Get timeline data.
        :rtype: object
        :return: timeline data
        """
        timeline = self.http.request(
            "feed/timeline/?rank_token=" + self.rank_token + "&ranked_content=true" +
            (("&max_id=" + str(maxid)) if maxid is not None else '')
        )[1]

        if timeline['status'] != 'ok':
            raise InstagramException(timeline['message'] + "\n")

        return timeline

    def getReelsTrayFeed(self):
        feed = ReelsTrayFeedResponse(self.http.request('feed/reels_tray/')[1])
        if not feed.isOk():
            raise InstagramException(feed.getMessage() + "\n")
            # return todo Unreachable code

        return feed

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
        userFeed = self.http.request("feed/user/" + str(usernameId) + "/?rank_token=" + self.rank_token
                                     + (("&max_id=" + str(maxid)) if maxid is not None else '') \
                                     + (("&minTimestamp=" + str(minTimestamp)) if minTimestamp is not None else '') \
                                     + "&ranked_content=true"
                                     )[1]

        if userFeed['status'] != 'ok':
            raise InstagramException(userFeed['message'] + "\n")

        return userFeed


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
        hashtagFeed = self.http.request(endpoint)[1]
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

        locationFeed = self.http.request(endpoint)[1]

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

        locationFeed = self.http.request(endpoint)[1]

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
        popularFeed = self.http.request("feed/popular/?people_teaser_supported=1&rank_token=" \
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
        return FollowingResponse(self.http.request(
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
        return FollowerResponse(self.http.request(
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
        return self.http.request("media/" + mediaId + "/like/", SignatureUtils.generateSignature(data))[1]

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
        return self.http.request("media/" + mediaId + "/unlike/", SignatureUtils.generateSignature(data))[1]

    def getMediaComments(self, mediaId, maxid=''):
        """
        Get media comments.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: Media comments data
        """
        return MediaCommentsResponse(self.http.request("media/" + str(mediaId) + "/comments/?max_id=" + str(maxid)
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

        return self.http.request("accounts/set_phone_and_name/", SignatureUtils.generateSignature(data))[1]

    def getDirectShare(self):
        """
        Get direct share.

        :rtype: object
        :return: Direct share data
        """
        return self.http.request('direct_share/inbox/?')[1]

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

        return self.http.request("friendships/create/" + userId + "/", SignatureUtils.generateSignature(data))[1]

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

        return self.http.request("friendships/destroy/" + userId + "/", SignatureUtils.generateSignature(data))[1]

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

        return self.http.request("friendships/block/" + userId + "/", SignatureUtils.generateSignature(data))[1]

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

        return self.http.request("friendships/unblock/" + userId + "/", SignatureUtils.generateSignature(data))[1]

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

        return self.http.request("friendships/show/" + userId + "/", SignatureUtils.generateSignature(data))[1]

    def getLikedMedia(self, maxid=None):
        """
        Get liked media.

        :rtype: object
        :return: Liked media data
        """
        endpoint = 'feed/liked/?' + (('max_id=' + str(maxid) + '&') if maxid is not None else '')
        return self.http.request(endpoint)[1]

    def verifyPeer(self, enable):
        self.http.verifyPeer(enable)

    def verifyHost(self, enable):
        self.http.verifyHost(enable)

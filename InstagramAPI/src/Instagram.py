import json
import pycurl
import time
import urllib
from collections import OrderedDict
from distutils.version import LooseVersion

import locale
import re

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from Utils import *
from http import HttpInterface, UserAgent
from http.Response import *

from InstagramException import InstagramException
from Constants import Constants
from SignatureUtils import SignatureUtils

locale.setlocale(locale.LC_NUMERIC, '')


class Instagram:
    def __init__(self, username, password, debug=False, IGDataPath=None):

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

        self.uuid = None  # // UUID
        self.device_id = None  # // Device ID
        self.username_id = None  # // Username ID
        self.token = None  # // _csrftoken
        self.isLoggedIn = False  # // Session status
        self.rank_token = None  # // Rank token
        self.IGDataPath = None  # // Data storage path
        self.http = None
        self.settings = None

        self.debug = debug
        self.device_id = SignatureUtils.generateDeviceId(hashlib.md5(username + password))

        if IGDataPath is not None:
            self.IGDataPath = IGDataPath
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

    def checkSettings(self,username):
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

    def login(self, force=False):
        """
        Login to Instagram.

        :type force: bool
        :param force: Force login to Instagram, this will create a new session
        :return: Login data
        :rtype List:
        """
        if (not self.isLoggedIn) or force:
            fetch = self.http.request(
                'si/fetch_headers/?challenge_type=signup&guid=' + SignatureUtils.generateUUID(False), None,True)

            if fetch[0] == '':
                raise InstagramException("Couldn't get challenge, check your connection")
                #return response #FIXME unreachable code

            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', fetch[0], re.MULTILINE)
            if match:
                self.token = match.group(1)

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
            self.getv2Inbox()
            self.getRecentActivity()

            return response

        check = self.timelineFeed()

        if 'message' in check and check['message'] == 'login_required':
            self.login(True)
        self.getv2Inbox()
        self.getRecentActivity()

    def syncFeatures(self):
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('id', self.username_id),
                ('_csrftoken', self.token),
                ('experiments', Constants.EXPERIMENTS)
            ])
        )
        return self.http.request('qe/sync/', SignatureUtils.generateSignature(data))[1]

    def autoCompleteUserList(self):
        return self.http.request('friendships/autocomplete_user_list/')[1]

    def timelineFeed(self):
        return self.http.request('feed/timeline/')[1]

    def megaphoneLog(self):
        return self.http.request('megaphone/log/')[1]

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
        return self.http.request('qe/expose/', SignatureUtils.generateSignature(data))[1]

    def logout(self):
        """
        Logout of Instagram.

        :rtype: bool
        :return: Returns true if logged out correctly
        """
        logout = self.http.request('accounts/logout/')
        return True if logout == 'ok' else False

    def uploadPhoto(self, photo, caption=None, upload_id=None):
        """
        Upload photo to Instagram.

        :type photo: str
        :param photo: Path to your photo
        :type caption: str
        :param caption: Caption to be included in your photo.
        :rtype: object
        :return: Upload data
        """
        return self.http.uploadPhoto(photo, caption, upload_id)

    def uploadVideo(self, video, caption=None):
        """
        Upload video to Instagram.

        :type video: str
        :param photo: Path to your video
        :type caption: str
        :param caption: Caption to be included in your video.
        :rtype: object
        :return: Upload data
        """
        return self.http.uploadVideo(video, caption)

    def direct_share(self, media_id, recipients, text=None):
        self.http.direct_share(media_id, recipients, text)

    def configureVideo(self, upload_id, video, caption=''):

        self.uploadPhoto(video, caption, upload_id)
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

    def configure(self, upload_id, photo, caption=''):

        size = Image.open(photo).size[0]

        post = json.dumps(
            OrderedDict([
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
        )
        post = post.replace('"crop_center":[0,0]', '"crop_center":[0.0,-0.0]')

        return ConfigureResponse(self.http.request('media/configure/', SignatureUtils.generateSignature(post))[1])

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
        return self.http.request("media/" + mediaId + "/edit_media/", SignatureUtils.generateSignature(data))[1]

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
        return self.http.request("usertags/" + mediaId + "/remove/", SignatureUtils.generateSignature(data))[1]

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
        return self.http.request("media/" + mediaId + "/comment/", SignatureUtils.generateSignature(data))[1]

    def deleteComment(self, mediaId, captionText, commentId):
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
                ('_csrftoken', self.token),
                ('caption_text', captionText)  # BUG!!!
            ])
        )
        return \
            self.http.request("media/" + mediaId + "/comment/" + commentId + "/delete/",
                              SignatureUtils.generateSignature(data))[
                1]

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
        return self.http.request('accounts/current_user/?edit=true', SignatureUtils.generateSignature(data))[1]

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

        return self.http.request('accounts/edit_profile/', SignatureUtils.generateSignature(data))[1]

    def getUsernameInfo(self, usernameId):
        """
        Get username info.
        :param usernameId: Username id
        :rtype: object
        :return: Username data
        """
        return self.http.request("users/" + str(usernameId) + "/info/")[1]

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
        activity = self.http.request('news/inbox/?')[1]

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
        He didn't know this yet.
        :rtype: object
        :return: v2 inbox data
        """
        inbox = self.http.request('direct_v2/inbox/?')[1]

        if inbox['status'] != 'ok':
            raise InstagramException(inbox['message'] + "\n")

        return inbox

    def getUserTags(self, usernameId):
        """
        Get user tags.
        :type usernameId: str
        :param usernameId:
        :rtype: object
        :return: user tags data
        """
        tags = self.http.request("usertags/" + str(usernameId) + "/feed/?rank_token=" + self.rank_token
                                 + "&ranked_content=true&")[1]
        if tags['status'] != 'ok':
            raise InstagramException(tags['message'] + "\n")

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
        userFeed = self.http.request("feed/tag/" + tag + "/?rank_token=" + self.rank_token + "&ranked_content=true&")[1]

        if userFeed['status'] != 'ok':
            raise InstagramException(userFeed['message'] + "\n")

        return userFeed

    def getMediaLikers(self, mediaId):
        """
        Get media likers.
        :type mediaId: str
        :param mediaId:
        :rtype: object
        :return:
        """
        likers = self.http.request("media/" + mediaId + "/likers/?")[1]
        if likers['status'] != 'ok':
            raise InstagramException(likers['message'] + "\n")

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
        query = self.http.request("users/" + usernameName + "/usernameinfo/")[1]

        if query['status'] != 'ok':
            raise InstagramException(query['message'] + "\n")

        return query

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

    def searchLocation(self, query):
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

    def getSelfUserFeed(self):
        """
        Get self user feed.
        :rtype: object
        :return: User feed data
        """
        return self.getUserFeed(self.username_id)

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
        return self.http.request(
            "friendships/" + usernameId + "/following/?max_id=" + maxid + "&ig_sig_key_version=" \
            + Constants.SIG_KEY_VERSION + "&rank_token=" + self.rank_token)[1]

    def getUserFollowers(self, usernameId, maxid=''):
        """
        Get user followers.
        :type usernameId: str
        :param usernameId: Username id

        :rtype: object
        :return: followers data
        """
        return self.http.request(
            "friendships/" + usernameId + "/followers/?max_id=" + maxid \
            + "&ig_sig_key_version=" + Constants.SIG_KEY_VERSION + "&rank_token=" + self.rank_token)[1]

    def getSelfUserFollowers(self):
        """
        Get self user followers.

        :rtype: object
        :return: followers data
        """
        return self.getUserFollowers(self.username_id)

    def getUsersFollowing(self):
        """
        Get self users we are following.

        :rtype: object
        :return: users we are following data
        """
        return self.http.request('friendships/following/?ig_sig_key_version=' \
                                 + Constants.SIG_KEY_VERSION + "&rank_token=" + self.rank_token)[1]

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

    def getMediaComments(self, mediaId):
        """
        Get media comments.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: Media comments data
        """
        return self.http.request("media/" + mediaId + "/comments/?")[1]

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
        myUploads = self.getSelfUserFeed()
        for item in myUploads['items']:
            dir_name = self.IGDataPath + 'backup/' + self.username + "-" + time.strftime('%Y-%m-%d')
            if os.path.isdir(dir_name):
                os.mkdir(dir_name)
            file_put_contents(
                os.path.join(dir_name, item['id'] + '.jpg'),
                urllib.urlopen(item['image_versions2']['candidates'][0]['url']).read()
            )  # todo test and remove below

            # urllib.urlretrieve(
            #    item['image_versions2']['candidates'][0]['url'],
            #    self.IGDataPath + 'backup/' + self.username + "-" + time.strftime('%Y-%m-%d') + '/' + item['id'] + '.jpg'
            # )

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

    def setProxy(self, proxy):
        self.http.setProxy(proxy)

    def setProxyPort(self, port):
        self.http.setProxyPort(port)

    def setProxyCredentials(self, username, password):
        self.http.setProxyCredentials(username, password)

    def clearProxy(self):
        self.http.clearProxy()
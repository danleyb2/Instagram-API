import hmac
import json
import locale
import pycurl
import re
import time
import math
import urllib

from collections import OrderedDict

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from src.InstagramException import InstagramException
from src.func import *
import Constants

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

        self.debug = debug
        self.device_id = self.generateDeviceId(hashlib.md5(username + password))
        if IGDataPath is not None:
            self.IGDataPath = IGDataPath
        else:
            self.IGDataPath = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
                ''
            )

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

        self.uuid = self.generateUUID(True)

        if os.path.isfile(self.IGDataPath + self.username + '-cookies.dat') and \
                os.path.isfile(self.IGDataPath + self.username + '-userId.dat') and \
                os.path.isfile(self.IGDataPath + self.username + '-token.dat'):
            self.isLoggedIn = True
            with open(self.IGDataPath + self.username + '-userId.dat', 'r') as userIdFile:
                self.username_id = userIdFile.read().strip()

            self.rank_token = self.username_id + '_' + self.uuid

            with open(self.IGDataPath + self.username + '-token.dat') as tokenFile:
                self.token = tokenFile.read().strip()

    def login(self, force=False):
        """
        Login to Instagram.

        :type force: bool
        :param force: Force login to Instagram, this will create a new session
        :return: Login data
        :rtype List:
        """
        if (not self.isLoggedIn) or force:
            fetch = self.request('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)
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

            login = self.request('accounts/login/', self.generateSignature(json.dumps(data)), True)
            if login[1]['status'] == 'fail': raise InstagramException(login[1]['message'])
            self.isLoggedIn = True
            self.username_id = str(login[1]['logged_in_user']['pk'])
            file_put_contents(self.IGDataPath + self.username + '-userId.dat', self.username_id)
            self.rank_token = self.username_id + '_' + self.uuid
            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', login[0], re.MULTILINE)
            if match: self.token = match.group(1)
            file_put_contents(self.IGDataPath + self.username + '-token.dat', self.token)

            self.syncFeatures()
            self.autoCompleteUserList()
            self.timelineFeed()
            self.getv2Inbox()
            self.getRecentActivity()

            return login[1]

        check = self.timelineFeed()

        if hasattr(check, 'message') and check['message'] == 'login_required':
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
        return self.request('qe/sync/', self.generateSignature(data))[1]

    def autoCompleteUserList(self):
        return self.request('friendships/autocomplete_user_list/')[1]

    def timelineFeed(self):
        return self.request('feed/timeline/')[1]

    def megaphoneLog(self):
        return self.request('megaphone/log/')[1]

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
        return self.request('qe/expose/', self.generateSignature(data))[1]

    def logout(self):
        """
        Login to Instagram.

        :rtype: bool
        :return: Returns true if logged out correctly
        """
        logout = self.request('accounts/logout/')
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
        endpoint = Constants.API_URL + 'upload/photo/'
        boundary = self.uuid

        if upload_id is not None:
            fileToUpload = createVideoIcon(photo)
        else:
            upload_id = locale.format("%.*f", (0, round(float('%.2f' % time.time()) * 1000)), grouping=False)
            fileToUpload = file_get_contents(photo)

        bodies = [
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'upload_id'),
                ('data', upload_id)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', '_uuid'),
                ('data', self.uuid)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', '_csrftoken'),
                ('data', self.token)
            ]),

            OrderedDict([
                ('type', 'form-data'),
                ('name', 'image_compression'),
                ('data', '{"lib_name":"jt","lib_version":"1.3.0","quality":"70"}')
            ]),

            OrderedDict([
                ('type', 'form-data'),
                ('name', 'photo'),
                ('data', fileToUpload),
                ('filename', 'pending_media_' + locale.format("%.*f", (0, round(float('%.2f' % time.time()) * 1000)),
                                                              grouping=False) + '.jpg'),
                ('headers', [
                    'Content-Transfer-Encoding: binary',
                    'Content-type: application/octet-stream',
                ])
            ]),
        ]

        data = self.buildBody(bodies, boundary)
        headers = [
            'Connection: close',
            'Accept: */*',
            'Content-type: multipart/form-data; boundary=' + boundary,
            'Content-Length: ' + str(len(data)),
            'Cookie2: $Version=1',
            'Accept-Language: en-US',
            'Accept-Encoding: gzip',
        ]

        buffer = BytesIO()
        ch = pycurl.Curl()

        ch.setopt(pycurl.URL, endpoint)
        ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + self.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + self.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        ch.close()

        header = resp[0: header_len]
        upload = json.loads(resp[header_len:])

        if upload['status'] == 'fail':
            raise InstagramException(upload['message'])

        if self.debug:
            print 'RESPONSE: ' + resp[header_len:] + "\n"

        configure = self.configure(upload['upload_id'], photo, caption)
        self.expose()

        return configure

    def uploadVideo(self, video, caption=None):

        videoData = file_get_contents(video)

        endpoint = Constants.API_URL + 'upload/video/'
        boundary = self.uuid
        upload_id = round(float('%.2f' % time.time()) * 1000)
        bodies = [
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'upload_id'),
                ('data', upload_id)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', '_csrftoken'),
                ('data', self.token)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'media_type'),
                ('data', 2)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', '_uuid'),
                ('data', self.uuid)
            ]),
        ]

        data = self.buildBody(bodies, boundary)
        headers = [
            'Connection: close',
            'Accept: */*',
            'Host: i.instagram.com',
            'Content-type: multipart/form-data; boundary=' + boundary,
            'Accept-Language: en-en',
        ]

        buffer = BytesIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, endpoint)
        ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + self.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + self.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)

        header = resp[0: header_len]
        body = json.loads(resp[header_len:])

        uploadUrl = body['video_upload_urls'][3]['url']
        job = body['video_upload_urls'][3]['job']

        request_size = int(math.floor(len(videoData) / 4.0))

        lastRequestExtra = (len(videoData) - (request_size * 4))

        for a in range(4):
            start = (a * request_size)
            end = (a + 1) * request_size + (lastRequestExtra if a == 3 else 0)

            headers = [
                'Connection: keep-alive',
                'Accept: */*',
                'Host: upload.instagram.com',
                'Cookie2: $Version=1',
                'Accept-Encoding: gzip, deflate',
                'Content-Type: application/octet-stream',
                'Session-ID: ' + str(upload_id),
                'Accept-Language: en-en',
                'Content-Disposition: attachment; filename="video.mov"',
                'Content-Length: ' + str(end - start),
                'Content-Range: ' + 'bytes ' + str(start) + '-' + str(end - 1) + '/' + str(len(videoData)),
                'job: ' + job,
            ]

            buffer = BytesIO()
            ch = pycurl.Curl()
            ch.setopt(pycurl.URL, uploadUrl)
            ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
            ch.setopt(pycurl.CUSTOMREQUEST, 'POST')
            ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
            ch.setopt(pycurl.FOLLOWLOCATION, True)
            ch.setopt(pycurl.HEADER, True)
            ch.setopt(pycurl.VERBOSE, False)
            ch.setopt(pycurl.HTTPHEADER, headers)
            ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + self.username + "-cookies.dat")
            ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + self.username + "-cookies.dat")
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, videoData[start:end])

            ch.perform()
            result = buffer.getvalue()
            header_len = ch.getinfo(pycurl.HEADER_SIZE)
            body = result[header_len:]
            # array.append([body]) todo fix

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        ch.close()

        header = resp[0: header_len]
        upload = json.loads(resp[header_len:])

        if upload['status'] == 'fail':
            raise InstagramException(upload['message'])

        if self.debug:
            print 'RESPONSE: ' + resp[header_len:] + "\n"

        configure = self.configureVideo(upload['upload_id'], video, caption)
        self.expose()

        return configure[1]

    def direct_share(self, media_id, recipients, text=None):
        if not isinstance(recipients, list):
            recipients = [recipients]

        string = []
        for recipient in recipients:
            string.append('"' + recipient + '"')

        recipeint_users = ','.join(string)

        endpoint = Constants.API_URL + 'direct_v2/threads/broadcast/media_share/?media_type=photo'
        boundary = self.uuid
        bodies = [
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'media_id'),
                ('data', media_id)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'recipient_users'),
                ('data', "[[" + recimient_users + "]]")  ##todo possible bug
            ]),

            OrderedDict([
                ('type', 'form-data'),
                ('name', 'client_context'),
                ('data', self.uuid)
            ]),

            OrderedDict([
                ('type', 'form-data'),
                ('name', 'thread_ids'),
                ('data', '["0"]')
            ]),

            OrderedDict([
                ('type', 'form-data'),
                ('name', 'text'),
                ('data', '' if text is None else text)
            ]),

        ]

        data = self.buildBody(bodies, boundary)
        headers = [
            'Proxy-Connection: keep-alive',
            'Connection: keep-alive',
            'Accept: */*',
            'Content-type: multipart/form-data boundary=' + boundary,
            'Accept-Language: en-en',
        ]

        buffer = BytesIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, endpoint)
        ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + self.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + self.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[0:header_len]
        upload = json.loads(resp[header_len:])
        ch.close()

    def configureVideo(self, upload_id, video, caption=''):

        self.uploadPhoto(video, '', upload_id)
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
                    ('length', getSeconds(video)),
                    ('source_type', '3'),
                    ('camera_position', 'back')
                ])),
                ('extra', OrderedDict([
                    ('source_width', 960),
                    ('source_height', 1280)
                ])),

                ('device', OrderedDict([
                    ('manufacturer', 'Xiaomi'),
                    ('model', 'HM 1SW'),
                    ('android_version', 18),
                    ('android_release', '4.3')
                ])),
                ('_csrftoken', self.token),
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('caption', caption)

            ])

        )

        post = post.replace('"length":0', '"length":0.00')

        return self.request('media/configure/?video=1', self.generateSignature(post))[1]

    def configure(self, upload_id, photo, caption=''):

        size = Image.open(photo).size[0]

        post = json.dumps(
            OrderedDict([
                ('upload_id', upload_id),
                ('camera_model', 'HM1S'),
                ('source_type', 3),
                ('date_time_original', time.strftime('%Y:%m:%d %H:%M:%S')),
                ('camera_make', 'XIAOMI'),
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
                    ('manufacturer', 'Xiaomi'),
                    ('model', 'HM 1SW'),
                    ('android_version', 18),
                    ('android_release', '4.3')
                ])),
                ('_csrftoken', self.token),
                ('_uuid', self.uuid),
                ('_uid', self.username_id),
                ('caption', caption)

            ])
        )
        post = post.replace('"crop_center":[0,0]', '"crop_center":[0.0,-0.0]')
        return self.request('media/configure/', self.generateSignature(post))[1]

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
        return self.request("media/" + mediaId + "/edit_media/", self.generateSignature(data))[1]

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
        return self.request("usertags/" + mediaId + "/remove/", self.generateSignature(data))[1]

    def mediaInfo(self, mediaId):
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
        return self.request("media/" + mediaId + "/info/", self.generateSignature(data))[1]

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
        return self.request("media/" + mediaId + "/delete/", self.generateSignature(data))[1]

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
        return self.request("media/" + mediaId + "/comment/", self.generateSignature(data))[1]

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
                ('_csrftoken', self.token),
                ('caption_text', captionText)  # BUG!!!
            ])
        )
        return self.request("media/" + mediaId + "/comment/" + commentId + "/delete/", self.generateSignature(data))[1]

    def changeProfilePicture(self, photo):
        """
        Sets account to public.
        :type photo: str
        :param photo: Path to photo
        """
        if photo is None:
            print ("Photo not valid")
            return

        uData = json.dumps(
            OrderedDict([
                ('_csrftoken', self.token),
                ('_uuid', self.uuid),
                ('_uid', self.username_id)
            ])
        )
        endpoint = Constants.API_URL + 'accounts/change_profile_picture/'
        boundary = self.uuid
        bodies = [
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'ig_sig_key_version'),
                ('data', Constants.SIG_KEY_VERSION)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'signed_body'),
                ('data', hmac.new(Constants.IG_SIG_KEY, uData, hashlib.sha256).hexdigest() + uData)]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'profile_pic'),
                ('data', file_get_contents(photo)),
                ('filename', 'profile_pic'),
                ('headers', [
                    'Content-type: application/octet-stream',
                    'Content-Transfer-Encoding: binary',
                ])
            ]),
        ]

        data = self.buildBody(bodies, boundary)
        headers = [
            'Proxy-Connection: keep-alive',
            'Connection: keep-alive',
            'Accept: */*',
            'Content-type: multipart/form-data; boundary=' + boundary,
            'Accept-Language: en-en',
            'Accept-Encoding: gzip, deflate',
        ]

        buffer = BytesIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, endpoint)
        ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + "self.username-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + "self.username-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)
        ch.perform()

        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[:header_len]
        upload = json.loads(resp[header_len:])

        ch.close()

    def removeProfilePicture(self):
        """
        Remove profile picture.
        :rtype: object
        :return: status request data
        """
        data = json.dumps(
            OrderedDict([('_uuid', self.uuid), ('_uid', self.username_id), ('_csrftoken', self.token)])
        )
        return self.request('accounts/remove_profile_picture/', self.generateSignature(data))[1]

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
        return self.request('accounts/set_private/', self.generateSignature(data))[1]

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
        return self.request('accounts/set_public/', self.generateSignature(data))[1]

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
        return self.request('accounts/current_user/?edit=true', self.generateSignature(data))[1]

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
                ('full_name', first_name),
                ('biography', biography),
                ('email', email),
                ('gender', gender)
            ])
        )

        return self.request('accounts/edit_profile/', self.generateSignature(data))[1]

    def getUsernameInfo(self, usernameId):
        """
        Get username info.
        :param usernameId: Username id
        :rtype: object
        :return: Username data
        """
        return self.request("users/" + usernameId + "/info/")[1]

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
        activity = self.request('news/inbox/?')[1]

        if activity['status'] != 'ok':
            raise InstagramException(activity['message'] + "\n")

        return activity

    def getFollowingRecentActivity(self):
        """
        Get recent activity from accounts followed.

        :rtype: object
        :return: Recent activity data of follows
        """
        activity = self.request('news/?')[1]
        if activity['status'] != 'ok':
            raise InstagramException(activity['message'] + "\n")

        return activity

    def getv2Inbox(self):
        """
        He didn't know this yet.
        :rtype: object
        :return: v2 inbox data
        """
        inbox = self.request('direct_v2/inbox/?')[1]

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
        tags = self.request("usertags/" + usernameId + "/feed/?rank_token=" + self.rank_token
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
        userFeed = self.request("feed/tag/" + tag + "/?rank_token=" + self.rank_token + "&ranked_content=true&")[1]

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
        likers = self.request("media/" + mediaId + "/likers/?")[1]
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
        locations = self.request("maps/user/" + usernameId + "/")[1]

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
        query = self.request("fbsearch/topsearch/?context=blended&query=" + query + "&rank_token=" + self.rank_token)[1]

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
        query = self.request(
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
        query = self.request("users/" + usernameName + "/usernameinfo/")[1]

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
            ('contacts', json.dumps(contacts))
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

    def getTimeline(self):
        """
        Get timeline data.
        :rtype: object
        :return: timeline data
        """
        timeline = self.request("feed/timeline/?rank_token=" + self.rank_token + "&ranked_content=true&")[1]

        if timeline['status'] != 'ok':
            raise InstagramException(timeline['message'] + "\n")

        return timeline

    def getUserFeed(self, usernameId):
        """
        Get user feed.
        :type usernameId: str
        :param usernameId: Username id
        :rtype: object
        :return: User feed data
        """
        userFeed = self.request("feed/user/" + usernameId + "/?rank_token=" \
                                + self.rank_token + "&ranked_content=true&")[1]

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
        hashtagFeed = self.request(endpoint)[1]
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
        return self.request(
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
        return self.request(
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
        return self.request('friendships/following/?ig_sig_key_version=' \
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
        return self.request("media/" + mediaId + "/like/", self.generateSignature(data))[1]

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
        return self.request("media/" + mediaId + "/unlike/", self.generateSignature(data))[1]

    def getMediaComments(self, mediaId):
        """
        Get media comments.
        :type mediaId: str
        :param mediaId: Media id
        :rtype: object
        :return: Media comments data
        """
        return self.request("media/" + mediaId + "/comments/?")[1]

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

        return self.request("accounts/set_phone_and_name/", self.generateSignature(data))[1]

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

        return self.request("friendships/create/" + userId + "/", self.generateSignature(data))[1]

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

        return self.request("friendships/destroy/" + userId + "/", self.generateSignature(data))[1]

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

        return self.request("friendships/block/" + userId + "/", self.generateSignature(data))[1]

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

        return self.request("friendships/unblock/" + userId + "/", self.generateSignature(data))[1]

    def getLikedMedia(self):
        """
        Get liked media.

        :rtype: object
        :return: Liked media data
        """
        return self.request('feed/liked/?')[1]

    def generateSignature(self, data):
        hash = hmac.new(Constants.IG_SIG_KEY, data, hashlib.sha256).hexdigest()

        return 'ig_sig_key_version=' + Constants.SIG_KEY_VERSION + \
               '&signed_body=' + hash + '.' + urllib.quote_plus(data)

    def generateDeviceId(self, seed):
        # // Neutralize username/password -> device correlation
        volatile_seed = '%d' % os.stat(os.path.dirname(os.path.realpath(__file__))).st_mtime

        return 'android-' + str(hashlib.md5(str(seed) + str(volatile_seed)))[16:]

    def generateUUID(self, type):
        uuid = '%04x%04x-%04x-%04x-%04x-%04x%04x%04x' % (
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        )

        return uuid if type else uuid.replace('-', '')

    def buildBody(self, bodies, boundary):
        body = ''
        for b in bodies:
            body += ('--' + boundary + "\r\n")
            body += ('Content-Disposition: ' + b['type'] + '; name="' + b['name'] + '"')
            if 'filename' in b:
                ext = os.path.splitext(b['filename'])[1][1:]
                body += ('; filename="' + 'pending_media_' + locale.format("%.*f", (
                    0, round(float('%.2f' % time.time()) * 1000)), grouping=False) + '.' + ext + '"')
            if 'headers' in b and isinstance(b['headers'], list):
                for header in b['headers']:
                    body += ("\r\n" + header)
            body += ("\r\n\r\n" + b['data'] + "\r\n")
        body += ('--' + boundary + '--')

        return body

    def request(self, endpoint, post=None, login=False):
        buffer = BytesIO()
        if (not self.isLoggedIn) and not login:
            raise InstagramException("Not logged in\n")

        headers = [
            'Connection: close',
            'Accept: */*',
            'Content-type: application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie2: $Version=1',
            'Accept-Language: en-US'
        ]

        ch = pycurl.Curl()

        ch.setopt(pycurl.URL, Constants.API_URL + endpoint)
        ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.VERBOSE, False)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + self.username + '-cookies.dat')
        ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + self.username + '-cookies.dat')

        if post:
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, post)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[0: header_len]
        body = resp[header_len:]
        ch.close()

        if self.debug:
            import urllib
            print "REQUEST: " + endpoint
            if post is not None:
                if not isinstance(post, list):
                    print 'DATA: ' + urllib.unquote_plus(post)
            print "RESPONSE: " + body + "\n"

        return [header, json.loads(body)]

import hmac
import json
import math
import pycurl
import time
from collections import OrderedDict

import locale

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from InstagramAPI.src.InstagramException import InstagramException
from InstagramAPI.src.Constants import Constants

from InstagramAPI.src.Utils import *
from InstagramAPI.src.http.Response import *


class HttpInterface(object):
    def __init__(self, parent):
        self.parent = None
        self.userAgent = None
        self.verifyPeer = False
        self.verifyHost = False

        self.parent = parent
        self.userAgent = self.parent.settings.get('user_agent')

    def request(self, endpoint, post=None, login=False):
        buffer = BytesIO()
        if (not self.parent.isLoggedIn) and not login:
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
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.VERBOSE, False)
        ch.setopt(pycurl.SSL_VERIFYPEER, self.verifyPeer)
        ch.setopt(pycurl.SSL_VERIFYHOST, self.verifyHost)
        ch.setopt(pycurl.COOKIEFILE, self.parent.IGDataPath + self.parent.username + '-cookies.dat')
        ch.setopt(pycurl.COOKIEJAR, self.parent.IGDataPath + self.parent.username + '-cookies.dat')

        if post:
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, post)

        if self.parent.proxy:
            ch.setopt(pycurl.PROXY, self.parent.proxyHost)
            if self.parent.proxyAuth:
                ch.setopt(pycurl.PROXYUSERPWD, self.parent.proxyAuth)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[0: header_len]
        body = resp[header_len:]
        ch.close()

        if self.parent.debug:
            import urllib
            print "REQUEST: " + endpoint
            if post is not None:
                if not isinstance(post, list):
                    print 'DATA: ' + urllib.unquote_plus(post)
            print "RESPONSE: " + body + "\n"

        return [header, json.loads(body)]

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
        boundary = self.parent.uuid

        if upload_id is not None:
            fileToUpload = Utils.createVideoIcon(photo)
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
                ('data', self.parent.uuid)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', '_csrftoken'),
                ('data', self.parent.token)
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
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.parent.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, self.verifyPeer)
        ch.setopt(pycurl.SSL_VERIFYHOST, self.verifyHost)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        if self.parent.proxy:
            ch.setopt(pycurl.PROXY, self.parent.proxyHost)
            if self.parent.proxyAuth:
                ch.setopt(pycurl.PROXYUSERPWD, self.parent.proxyAuth)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)

        header = resp[0: header_len]
        upload = UploadPhotoResponse(json.loads(resp[header_len:]))

        ch.close()

        if not upload.isOk():
            raise InstagramException(upload.getMessage())

        if self.parent.debug:
            print 'RESPONSE: ' + resp[header_len:] + "\n"

        configure = self.parent.configure(upload.getUploadId(), photo, caption)

        if not configure.isOk():
            raise InstagramException(configure.getMessage())

        self.parent.expose()

        return configure

    def uploadVideo(self, video, caption=None):

        videoData = file_get_contents(video)

        endpoint = Constants.API_URL + 'upload/video/'
        boundary = self.parent.uuid
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
                ('data', self.parent.token)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'media_type'),
                ('data', 2)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', '_uuid'),
                ('data', self.parent.uuid)
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
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.parent.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        if self.parent.proxy:
            ch.setopt(pycurl.PROXY, self.parent.proxyHost)
            if self.parent.proxyAuth:
                ch.setopt(pycurl.PROXYUSERPWD, self.parent.proxyAuth)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)

        header = resp[0: header_len]
        body = UploadJobVideoResponse(json.loads(resp[header_len:]))

        uploadUrl = body.getVideoUploadUrl()
        job = body.getVideoUploadJob()

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
            ch.setopt(pycurl.USERAGENT, self.userAgent)
            ch.setopt(pycurl.CUSTOMREQUEST, 'POST')
            ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
            ch.setopt(pycurl.FOLLOWLOCATION, True)
            ch.setopt(pycurl.HEADER, True)
            ch.setopt(pycurl.VERBOSE, False)
            ch.setopt(pycurl.HTTPHEADER, headers)
            ch.setopt(pycurl.COOKIEFILE, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
            ch.setopt(pycurl.COOKIEJAR, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, videoData[start:end])

            if self.parent.proxy:
                ch.setopt(pycurl.PROXY, self.parent.proxyHost)
                if self.parent.proxyAuth:
                    ch.setopt(pycurl.PROXYUSERPWD, self.parent.proxyAuth)

            ch.perform()
            result = buffer.getvalue()
            header_len = ch.getinfo(pycurl.HEADER_SIZE)
            body = result[header_len:]
            # array.append([body]) todo fix

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)

        header = resp[0: header_len]
        upload = UploadVideoResponse(json.loads(resp[header_len:]))

        ch.close()

        if self.parent.debug:
            print 'RESPONSE: ' + resp[header_len:] + "\n"

        configure = self.parent.configureVideo(upload['upload_id'], video, caption)
        self.parent.expose()

        return configure[1]

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
                ('_csrftoken', self.parent.token),
                ('_uuid', self.parent.uuid),
                ('_uid', self.parent.username_id)
            ])
        )
        endpoint = Constants.API_URL + 'accounts/change_profile_picture/'
        boundary = self.parent.uuid
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
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.parent.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, self.verifyPeer)
        ch.setopt(pycurl.SSL_VERIFYHOST, self.verifyHost)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        if self.parent.proxy:
            ch.setopt(pycurl.PROXY, self.parent.proxyHost)
            if self.parent.proxyAuth:
                ch.setopt(pycurl.PROXYUSERPWD, self.parent.proxyAuth)

        ch.perform()

        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[:header_len]
        upload = json.loads(resp[header_len:])

        ch.close()

    def direct_share(self, media_id, recipients, text=None):
        if not isinstance(recipients, list):
            recipients = [recipients]

        string = []
        for recipient in recipients:
            string.append('"' + recipient + '"')

        recipient_users = ','.join(string)

        endpoint = Constants.API_URL + 'direct_v2/threads/broadcast/media_share/?media_type=photo'
        boundary = self.parent.uuid
        bodies = [
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'media_id'),
                ('data', media_id)
            ]),
            OrderedDict([
                ('type', 'form-data'),
                ('name', 'recipient_users'),
                ('data', "[[" + recipient_users + "]]")
            ]),

            OrderedDict([
                ('type', 'form-data'),
                ('name', 'client_context'),
                ('data', self.parent.uuid)
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
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, self.parent.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, self.verifyPeer)
        ch.setopt(pycurl.SSL_VERIFYHOST, self.verifyHost)
        ch.setopt(pycurl.HTTPHEADER, headers)
        ch.setopt(pycurl.COOKIEFILE, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.COOKIEJAR, self.parent.IGDataPath + self.parent.username + "-cookies.dat")
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.POSTFIELDS, data)

        if self.parent.proxy:
            ch.setopt(pycurl.PROXY, self.parent.proxyHost)
            if self.parent.proxyAuth:
                ch.setopt(pycurl.PROXYUSERPWD, self.parent.proxyAuth)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[0:header_len]
        upload = json.loads(resp[header_len:])
        ch.close()

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

    def verifyPeer(self, enable):
        self.verifyPeer = enable

    def verifyHost(self, enable):
        self.verifyHost = enable

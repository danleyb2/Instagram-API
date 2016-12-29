import json
import pycurl
from collections import OrderedDict

import re

from InstagramAPI.src import InstagramException
from InstagramAPI.src import SignatureUtils
from InstagramAPI.src.http.Response import ChallengeResponse
from InstagramAPI.src.http.Response.AccountCreationResponse import AccountCreationResponse
from InstagramAPI.src.http.Response.CheckEmailResponse import CheckEmailResponse
from InstagramAPI.src.http.Response.CheckUsernameResponse import CheckUsernameResponse
from InstagramAPI.src.http.Response.UsernameSuggestionsResponse import UsernameSuggestionsResponse

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from Constants import Constants
from Utils import *


class InstagramRegistration(object):
    def __init__(self, debug=False, IGDataPath=None):

        self.debug = None
        self.IGDataPath = None
        self.username = None
        self.uuid = None
        self.waterfall_id = None
        self.token = None
        self.userAgent = None
        self.settings = None
        self.proxy = None  # Full Proxy
        self.proxyHost = None  # Proxy Host and Port
        self.proxyAuth = None  # Proxy User and Pass

        self.username = ''
        self.debug = debug
        self.uuid = SignatureUtils.generateUUID(True)
        self.waterfall_id = SignatureUtils.generateUUID(True)

        if IGDataPath is not None:
            self.IGDataPath = IGDataPath
        else:
            self.IGDataPath = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
                ''
            )

        self.userAgent = 'Instagram ' + Constants.VERSION + ' Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'

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

    def checkUsername(self, username):
        """
        Checks if the username is already taken (exists).
        :type username: str
        :param username:
        :rtype: object
        :return: Username availability data
        """
        data = json.dumps(
            OrderedDict([
                ('_uuid', self.uuid),
                ('username', username),
                ('_csrftoken', 'missing'),
            ])
        )

        self.username = username
        self.settings = Settings(os.path.join(self.IGDataPath, self.username, 'settings-' + username + '.dat'))
        return CheckUsernameResponse(self.request('users/check_username/', SignatureUtils.generateSignature(data))[1])

    def checkEmail(self, email):

        data = json.dumps(
            OrderedDict([
                ('qe_id', SignatureUtils.generateUUID(True)),
                ('waterfall_id', SignatureUtils.generateUUID(True)),
                ('email', email),
                ('_csrftoken', 'missing'),
            ])
        )

        return CheckEmailResponse(self.request('users/check_email/', SignatureUtils.generateSignature(data))[1])

    def usernameSuggestions(self, email, name):
        data = json.dumps(
            OrderedDict([
                ('name', SignatureUtils.generateUUID(True)),
                ('waterfall_id', SignatureUtils.generateUUID(True)),
                ('email', email),
                ('_csrftoken', 'missing'),
            ])
        )

        return UsernameSuggestionsResponse(
            self.request('accounts/username_suggestions/', SignatureUtils.generateSignature(data))[1])

    def createAccount(self, username, password, email, name=''):
        """
        Register account.
        :type username: str
        :param username:
        :type password: str
        :param password:
        :type email: str
        :param email:

        :rtype: object
        :return: Registration data
        """

        token = self.getCsfrtoken()
        data = json.dumps(
            OrderedDict([
                ('allow_contacts_sync', 'true'),
                ('phone_id', self.uuid),
                ('_csrftoken', token),
                ('username', username),
                ('first_name', name),
                ('guid', self.uuid),
                ('device_id', SignatureUtils.generateDeviceId(hashlib.md5(username + password).hexdigest())),
                ('email', email),
                ('force_sign_up_code', ''),
                ('waterfall_id', self.waterfall_id),
                ('qs_stamp', ''),
                ('password', password),
            ])
        )

        result = self.request('accounts/create/', SignatureUtils.generateSignature(data))
        header = result[0]
        response = AccountCreationResponse(result[1])

        if response.isAccountCreated():
            self.username_id = response.getUsernameId()
            self.settings.set('username_id', self.username_id)
            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', header, re.MULTILINE)
            token = match.group(1) if match else ''
            self.settings.set('token', token)

        return response

    def getCsfrtoken(self):

        fetch = self.request('si/fetch_headers/', None, True)

        header = fetch[0]
        response = ChallengeResponse(fetch[1])

        if not header or not response.isOk():
            raise InstagramException("Couldn't get challenge, check your connection")
            # return response #fixme unreachable code

        match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', fetch[0], re.MULTILINE)

        if not match:
            raise InstagramException("Missing csfrtoken")
            # return $response #fixme unreachable code

        token = match.group(1)
        return token[22:]

    def request(self, endpoint, post=None):
        buffer = BytesIO()

        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, Constants.API_URL + endpoint)
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, False)
        ch.setopt(pycurl.COOKIEFILE, os.path.join(self.IGDataPath, self.username, self.username + "-cookies.dat"))
        ch.setopt(pycurl.COOKIEJAR, os.path.join(self.IGDataPath, self.username, self.username + "-cookies.dat"))

        if post is not None:
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, post)

        if self.proxy:
            ch.setopt(pycurl.PROXY, self.proxyHost)
            if self.proxyAuth:
                ch.setopt(pycurl.PROXYUSERPWD, self.proxyAuth)

        ch.perform()
        resp = buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[0: header_len]
        body = resp[header_len:]

        ch.close()

        if self.debug:
            print "REQUEST: " + endpoint
            if post is not None:
                if not isinstance(post, list):
                    print "DATA: " + str(post)
            print "RESPONSE: " + body

        return [header, json_decode(body)]

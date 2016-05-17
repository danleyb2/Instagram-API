import hashlib
import hmac
import json
import os
import pycurl
import urllib
import re
from collections import OrderedDict

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from src import Constants
from php import *


class InstagramRegistration(object):
    def __init__(self, debug=False, IGDataPath=None):

        self.debug = None
        self.IGDataPath = None
        self.username = None
        self.uuid = None

        self.username = ''
        self.debug = debug
        self.uuid = self.generateUUID(True)

        if IGDataPath is not None:
            self.IGDataPath = IGDataPath
        else:
            self.IGDataPath = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
                ''
            )

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
        return self.request('users/check_username/', self.generateSignature(data))[1]

    def createAccount(self, username, password, email):
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
        data = json.dumps(
            OrderedDict([
                ('phone_id', self.uuid),
                ('_csrftoken', 'missing'),
                ('username', username),
                ('first_name', ''),
                ('guid', self.uuid),
                ('device_id', 'android-' + filter(
                    None, re.split('(.{1,17})', hashlib.md5(str(mt_rand(1000, 9999))).hexdigest()))[mt_rand(0, 1)]),
                ('email', email),
                ('force_sign_up_code', ''),
                ('qs_stamp', ''),
                ('password', password),
            ])
        )

        result = self.request('accounts/create/', self.generateSignature(data))

        if hasattr(result[1], 'account_created') and result[1]['account_created'] == True:
            self.username_id = result[1]['created_user']['pk']
            file_put_contents(self.IGDataPath + username + "-userId.dat", self.username_id)
            match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', result[0], re.MULTILINE)
            token = match.group(1) if match else ''
            self.username = username
            file_put_contents(self.IGDataPath + username + "-token.dat", token)
            os.rename(self.IGDataPath + 'cookies.dat', self.IGDataPath + username + "-cookies.dat")

        return result

    def generateSignature(self, data):

        hash_var_renamed = hmac.new(Constants.IG_SIG_KEY, data,
                                    hashlib.sha256).hexdigest()  # todo renamed variable hash

        return 'ig_sig_key_version=' + Constants.SIG_KEY_VERSION + '&signed_body=' + hash_var_renamed + '.' + urllib.quote_plus(
            data)

    def generateUUID(self, type):  ##todo finish mt_rand
        uuid = '%04x%04x-%04x-%04x-%04x-%04x%04x%04x' % (
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        )
        return uuid if type else uuid.replace('-', '')

    def request(self, endpoint, post=None):
        buffer = BytesIO()

        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, Constants.API_URL + endpoint)
        ch.setopt(pycurl.USERAGENT, Constants.USER_AGENT)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, False)
        if os.path.isfile(self.IGDataPath + self.username + "-cookies.dat"):
            ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + self.username + "-cookies.dat")
            ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + self.username + "-cookies.dat")
        else:
            ch.setopt(pycurl.COOKIEFILE, self.IGDataPath + 'cookies.dat')
            ch.setopt(pycurl.COOKIEJAR, self.IGDataPath + 'cookies.dat')

        if post is not None:
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, post)

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

        return [header, json.loads(body)]

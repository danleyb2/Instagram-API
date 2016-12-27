import json
import pycurl
from collections import OrderedDict

import os
import re

from InstagramAPI.src.Utils import Settings, json_decode

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class Checkpoint(object):
    def __init__(self, username, settingsPath=None, debug=False):
        self.username = None
        self.settingsPath = None
        self.settings = None
        self.userAgent = None
        self.debug = None

        self.username = username
        self.debug = debug

        if not settingsPath:
            self.settingsPath = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
                username,
                ''
            )
            if not os.path.isdir(self.settingsPath): os.mkdir(self.settingsPath, 0777)

        self.settings = Settings(self.settingsPath + 'settings-' + username + '.dat')
        self.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34 Instagram 8.5.2 (iPhone5,2; iPhone OS 9_3_3; es_ES; es-ES; scale=2.00; 640x1136)'

    def doCheckpoint(self):
        token = self.checkpointFirstStep()
        self.checkpointSecondStep(token)

        return token

    def checkpointFirstStep(self):
        response = self.request("https://i.instagram.com/integrity/checkpoint/checkpoint_logged_out_main/" +
                                str(self.settings.get('username_id')) + "/?next=instagram%3A%2F%2Fcheckpoint%2Fdismiss")

        # Fixme str value of null is '' in php ,str value of None is 'None' in python
        match = re.search(r'^Set-Cookie: csrftoken=([^;]+)', response[0], re.MULTILINE)

        if match:
            token = match.group(1)
            return token

        return None

    def checkpointSecondStep(self, token):
        post = OrderedDict([
            ('csrfmiddlewaretoken', token),  # fixme php version is the matched array at this point
            ('email', 'Verificar por correo electronico')  # google translates to Verify by email
        ])

        headers = [
            'Origin: https://i.instagram.com',
            'Connection: keep-alive',
            'Proxy-Connection: keep-alive',
            'Accept-Language: es-es',

            'Referer: https://i.instagram.com/integrity/checkpoint/checkpoint_logged_out_main/' +
            str(self.settings.get('username_id')) + '/?next=instagram%3A%2F%2Fcheckpoint%2Fdismiss',

            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        ]

        self.request(
            'https://i.instagram.com/integrity/checkpoint/checkpoint_logged_out_main/' +
            str(self.settings.get('username_id')) + '/?next=instagram%3A%2F%2Fcheckpoint%2Fdismiss',
            headers,
            post
        )

        return token

    def checkpointThird(self, code, token):
        post = OrderedDict([
            ('csrfmiddlewaretoken', token),
            ('response_code', code)
        ])

        headers = [
            'Origin: https://i.instagram.com',
            'Connection: keep-alive',
            'Proxy-Connection: keep-alive',
            'Accept-Language: es-es',

            'Referer: https://i.instagram.com/integrity/checkpoint/checkpoint_logged_out_main/' +
            str(self.settings.get('username_id')) + '/?next=instagram%3A%2F%2Fcheckpoint%2Fdismiss',

            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        ]

        self.request(
            'https://i.instagram.com/integrity/checkpoint/checkpoint_logged_out_main/' +
            str(self.settings.get('username_id')) +
            '/?next=instagram%3A%2F%2Fcheckpoint%2Fdismiss',
            headers,
            post
        )

    def request(self, endpoint, headers=None, post=None, first=True):
        buffer = BytesIO()

        ch = pycurl.Curl()

        ch.setopt(pycurl.URL, endpoint)
        ch.setopt(pycurl.USERAGENT, self.userAgent)
        ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        if headers:
            ch.setopt(pycurl.HTTPHEADER, headers)

        ch.setopt(pycurl.VERBOSE, self.debug)
        ch.setopt(pycurl.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.SSL_VERIFYHOST, False)
        ch.setopt(pycurl.COOKIEFILE, self.settingsPath + self.username + '-cookies.dat')
        ch.setopt(pycurl.COOKIEJAR, self.settingsPath + self.username + '-cookies.dat')

        if post:
            import urllib
            ch.setopt(pycurl.POST, len(post))
            ch.setopt(pycurl.POSTFIELDS, urllib.urlencode(post))

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
                    print 'DATA: ' + urllib.unquote_plus(json.dumps(post))
            print "RESPONSE: " + body + "\n"

        return [header, json_decode(body)]

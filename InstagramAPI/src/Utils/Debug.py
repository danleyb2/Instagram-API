from InstagramAPI.src.Python import *
from Utils import Utils

class Debug():
    @staticmethod
    def printRequest(method, endpoint):
        if php_sapi_name() == 'cli':
            method = Utils.colouredString("method:  ", 'light_blue')
        else:
            method = method + ':  '
        echo(method + endpoint + "\n")

    @staticmethod
    def printUpload(uploadBytes):
        if php_sapi_name() == 'cli':
            dat = Utils.colouredString('→ ' + uploadBytes, 'yellow')
        else:
            dat = '→ ' + uploadBytes
        echo(dat + "\n")

    @staticmethod
    def printHttpCode(httpCode, bytes_):
        if php_sapi_name() == 'cli':
            echo(Utils.colouredString("← " + httpCode + " \t " + bytes_, 'green') + "\n")
        else:
            echo("← " + httpCode + " \t " + bytes_ + "\n")

    @staticmethod
    def printResponse(response, truncated=False):
        if php_sapi_name() == 'cli':
            res = Utils.colouredString('RESPONSE: ', 'cyan')
        else:
            res = 'RESPONSE: '
        if truncated and len(response) > 1000:
            response = response[0:1000] + '...'
        echo(res + response + "\n\n")

    @staticmethod
    def printPostData(post):
        if php_sapi_name() == 'cli':
            dat = Utils.colouredString('DATA: ', 'yellow')
        else:
            dat = 'DATA: '
        echo(dat + urldecode(post) + "\n")

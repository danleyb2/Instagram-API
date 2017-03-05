from PIL import Image
import hashlib
import json
from .Compat import *
import os
import os.path
import shutil
import hmac
import sys


def is_dir(path):
    return os.path.isdir(path)


def mkdir(path):
    return os.mkdir(path)


def filemtime(path):
    return os.stat(path).st_mtime


def copy(src, dest):
    if "://" in src:
        file_put_contents(
            dest,
            compat_urllib_request.urlopen(src).read()
        )
    else:
        shutil.copy2(src, dest)


def file_get_contents(file):
    with open(file, 'rb') as fFile:
        return fFile.read()


def file_put_contents(file, contents):
    with open(file, 'w') as fFile:
        fFile.write(contents)  ##todo return result
        fFile.flush()


def mt_rand(low=0, high=0x7fffffff):
    import random
    return random.randint(low, high)


def exec_php(cmd):
    from subprocess import Popen, PIPE, STDOUT
    p = Popen(cmd, shell=False, stdout=PIPE, stderr=STDOUT)
    return [p.wait(), p.stdout.readlines()]


def parse_url(url):
    import urlparse
    r = urlparse.urlparse(url)._asdict()  # Fixme Access to a protected member _asdict() of a class
    r['host'] = r['netloc']
    return r


def json_encode(data):
    try:
        return json.dumps(data)
    except ValueError:
        return None


def json_decode(json_string):
    try:
        return json.loads(json_string)
    except ValueError:
        return None


def getimagesize(photo):
    return Image.open(photo).size


def md5(string):
    return str(hashlib.md5(string.encode("utf-8")).hexdigest())


def urlencode(string):
    return compat_urllib_parse.quote_plus(string)


def urldecode(string):
    return compat_urllib_parse.unquote_plus(string)


def rawurlencode(string):
    return compat_urllib_parse.quote(string)


def rawurldecode(string):
    return compat_urllib_parse.unquote(string)


def http_build_query(params):
    return compat_urllib_parse.urlencode(params)


def hash_hmac(algo_str, data, key):
    algo = None
    if algo_str == "sha256":
        algo = hashlib.sha256

    return hmac.new(key.encode("utf-8"), data.encode("utf-8"), algo).hexdigest()


def php_sapi_name():
    return "cli" # FIXME


def echo(text):
    sys.stdout.write(text)

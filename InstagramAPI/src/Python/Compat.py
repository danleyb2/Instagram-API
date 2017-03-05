# From https://github.com/rg3/youtube-dl/blob/master/youtube_dl/compat.py

try:
    import urllib.parse as compat_urllib_parse
except ImportError:  # Python 2
    import urllib as compat_urllib_parse


try:
    import urllib.request as compat_urllib_request
except ImportError:  # Python 2
    import urllib as compat_urllib_request

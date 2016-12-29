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


def json_decode(json_string):
    import json
    try:
        return json.loads(json_string)
    except ValueError:
        return None

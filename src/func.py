import hashlib
import os
from tempfile import mkdtemp

from PIL import Image

from src.php import *


def exec2(cmd):
    from subprocess import Popen, PIPE, STDOUT
    p = Popen(cmd, shell=False, stdout=PIPE, stderr=STDOUT)
    return [p.wait(), p.stdout.readlines()]


def getSeconds(file):
    ffmpeg = checkFFMPEG()
    if ffmpeg:
        time = exec2([ffmpeg, '-i', file, '2>&1', '|', 'grep', 'Duration', '|', 'cut', '-d', '-f', '4'])[1]
        duration = time.split(":")
        seconds = duration[0] * 3600 + duration[1] * 60 + round(duration[2])
        return seconds

    return mt_rand(15, 300)


def checkFFMPEG():
    try:
        return_value = exec2(['ffmpeg', '-version', '2>&1'])[0]
        if return_value == 0: return "ffmpeg"

        return_value = exec2(['avconv', '-version', '2>&1'])[0]
        if return_value == 0: return "avconv"
    except Exception:
        pass

    return False


def createVideoIcon(file):
    # should install ffmpeg for the method to work successfully
    ffmpeg = checkFFMPEG()

    if ffmpeg:
        # generate thumbnail
        preview = os.path.join(mkdtemp(), hashlib.md5(file) + '.jpg')

        try:os.unlink(preview)
        except Exception:pass

        # capture video preview
        command = [ffmpeg, '-i', file, '-f', 'mjpeg', '-ss', '00:00:01', '-vframes', '1', preview, '2>&1']
        exec2(command)
        return createIconGD(preview)


def createIconGD(file, size=100, raw=True):
    image = Image.open(file)
    width, height = image.size

    if width > height:
        y = 0
        x = (width - height) / 2
        smallestSide = height
    else:
        x = 0
        y = (height - width) / 2
        smallestSide = width

    # image_p = Image.new('RGB',(size, size))
    # image = Image.frombytes('RGBa',(size,size),file_get_contents(file))

    image.thumbnail((size, size))

    ##todo convert to jpeg
    i = image.tobytes()
    image.close()
    # image_p.close()
    return i

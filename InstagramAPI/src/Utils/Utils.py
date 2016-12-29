import hashlib
from tempfile import mkdtemp

import os
from PIL import Image

from php import *


class Utils:
    @staticmethod
    def getSeconds(file):
        """
        Length of the file in Seconds

        :type file: str
        :param file: path to the file name
        :return: length of the file in seconds
        """
        ffmpeg = Utils.checkFFMPEG()
        if ffmpeg:
            time = exec_php([ffmpeg, '-i', file, '2>&1', '|', 'grep', 'Duration', '|', 'cut', '-d', '-f', '4'])[1]
            duration = time.split(":")
            seconds = duration[0] * 3600 + duration[1] * 60 + round(duration[2])
            return seconds

        return mt_rand(15, 300)

    @staticmethod
    def checkFFMPEG():
        """
        Check for ffmpeg/avconv dependencies

        :rtype: str/bool
        :return: name of the library if present, false otherwise
        """
        try:
            return_value = exec_php(['ffmpeg', '-version', '2>&1'])[0]
            if return_value == 0: return "ffmpeg"

            return_value = exec_php(['avconv', '-version', '2>&1'])[0]
            if return_value == 0: return "avconv"
        except Exception:
            pass

        return False

    @staticmethod
    def createVideoIcon(file):
        """
        Creating a video icon/thumbnail

        :type file: str
        :param file: path to the file name
        :rtype: image
        :return: icon/thumbnail for the video
        """
        # should install ffmpeg for the method to work successfully
        ffmpeg = Utils.checkFFMPEG()

        if ffmpeg:
            # generate thumbnail
            preview = os.path.join(mkdtemp(), hashlib.md5(file) + '.jpg')

            try:
                os.unlink(preview)
            except Exception:
                pass

            # capture video preview
            command = [ffmpeg, '-i', file, '-f', 'mjpeg', '-ss', '00:00:01', '-vframes', '1', preview, '2>&1']
            exec_php(command)
            return file_get_contents(preview)

    @staticmethod
    def createIconGD(file, size=100, raw=True):
        """
        Implements the actual logic behind creating the icon/thumbnail

        :type file: str
        :param file: path to the file name
        :rtype: image
        :return: icon/thumbnail for the video
        """
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

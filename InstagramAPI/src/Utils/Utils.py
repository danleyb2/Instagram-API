import hashlib
import os
from PIL import Image
from tempfile import mkdtemp

from .php import *


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

    @staticmethod
    def formatBytes(bytes_, precision=2):
        import math
        units = ('B', 'kB', 'mB', 'gB', 'tB')
        bytes_ = max(bytes_, 0)
        pow_ = math.floor((math.log(bytes_) if bytes_ else 0) / math.log(1024))
        pow_ = min(pow_, len(units) - 1)
        bytes_ /= math.pow(1024, pow_)
        return str(round(bytes_, precision)) + ' ' + units[int(pow_)]

    @staticmethod
    def colouredString(string, colour):
        colours = dict()

        colours['black'] = '0;30'
        colours['dark_gray'] = '1;30'
        colours['blue'] = '0;34'
        colours['light_blue'] = '1;34'
        colours['green'] = '0;32'
        colours['light_green'] = '1;32'
        colours['cyan'] = '0;36'
        colours['light_cyan'] = '1;36'
        colours['red'] = '0;31'
        colours['light_red'] = '1;31'
        colours['purple'] = '0;35'
        colours['light_purple'] = '1;35'
        colours['brown'] = '0;33'
        colours['yellow'] = '1;33'
        colours['light_gray'] = '0;37'
        colours['white'] = '1;37'

        colored_string = ""

        if colour in colours:
            colored_string += "\033[" + colours[colour] + "m"

        colored_string += string + "\033[0m"
        return colored_string

    @staticmethod
    def getFilterCode():

        filters = []
        filters[108] = "Charmes"
        filters[116] = "Ashby"
        filters[117] = "Helena"
        filters[115] = "Brooklyn"
        filters[105] = "Dogpatch"
        filters[113] = "Skyline"
        filters[107] = "Ginza"
        filters[118] = "Maven"
        filters[16] = "Kelvin"
        filters[14] = "1977"
        filters[20] = "Walden"
        filters[19] = "Toaster"
        filters[18] = "Sutro"
        filters[22] = "Brannan"
        filters[3] = "Earlybird"
        filters[106] = "Vesper"
        filters[109] = "Stinson"
        filters[15] = "Nashville"
        filters[21] = "Hefe"
        filters[10] = "Inkwell"
        filters[2] = "Lo-Fi"
        filters[28] = "Willow"
        filters[27] = "Sierra"
        filters[1] = "X Pro II"
        filters[25] = "Valencia"
        filters[26] = "Hudson"
        filters[23] = "Rise"
        filters[17] = "Mayfair"
        filters[24] = "Amaro"
        filters[608] = "Perpetua"
        filters[612] = "Aden"
        filters[603] = "Ludwig"
        filters[616] = "Crema"
        filters[605] = "Slumber"
        filters[613] = "Juno"
        filters[614] = "Reyes"
        filters[615] = "Lark"
        filters[111] = "Moon"
        filters[114] = "Gingham"
        filters[112] = "Clarendon"
        filters[0] = "Normal"

        return filters.index(filter)

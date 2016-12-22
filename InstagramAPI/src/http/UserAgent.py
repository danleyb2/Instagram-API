from InstagramAPI.src import Constants
from InstagramAPI.src.Utils import *


class UserAgent:
    def __init__(self, parent):
        self.parent = None

        self.parent = parent

    def getDeviceData(self):
        csvfile = os.path.join(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'devices.csv')
        )
        line_of_text = []
        with open(csvfile, 'rb') as file_handle:
            for line in file_handle.readlines():
                line_of_text.append(line.strip())
        # todo doesn't look like original
        deviceData = (line_of_text[mt_rand(0, 11867)]).split(';')
        return deviceData

    def buildUserAgent(self):
        deviceData = self.getDeviceData()

        self.parent.settings.set('manufacturer', deviceData[0])
        self.parent.settings.set('device', deviceData[1])
        self.parent.settings.set('model', deviceData[2])

        return 'Instagram %s Android (18/4.3; 320dpi; 720x1280; %s; %s; %s; qcom; en_US)' % (
            Constants.VERSION, deviceData[0], deviceData[1], deviceData[2])

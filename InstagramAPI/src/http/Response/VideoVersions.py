class VideoVersions(object):
    def __init__(self, response):
        self.url = None
        self.type = None
        self.width = None
        self.height = None

        self.url = response['url']
        self.type = response['type']
        self.width = response['width']
        self.height = response['height']

    def getUrl(self):
        return self.url

    def getType(self):
        return self.type

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

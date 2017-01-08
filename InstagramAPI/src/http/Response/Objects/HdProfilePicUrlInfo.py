class HdProfilePicUrlInfo(object):
    def __init__(self, response):
        self.url = None
        self.width = None
        self.height = None

        self.url = response['url']
        self.width = response['width']
        self.height = response['height']

    def getUrl(self):
        return self.url

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

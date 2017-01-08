class Suggestion(object):
    def __init__(self, data):
        self.media_infos = None
        self.social_context = None
        self.algorithm = None
        self.thumbnail_urls = None
        self.value = None
        self.caption = None
        self.user = None
        self.large_urls = None
        self.media_ids = None
        self.icon = None

        self.media_infos = data['media_infos']
        self.social_context = data['social_context']
        self.algorithm = data['algorithm']
        self.thumbnail_urls = data['thumbnail_urls']
        self.value = data['value']
        self.caption = data['caption']
        self.user = User(data['user'])
        self.large_urls = data['large_urls']
        self.media_ids = data['media_ids']
        self.icon = data['icon']

    def getMediaInfo(self):
        return self.media_infos

    def getSocialContext(self):
        return self.social_context

    def getalgorithm(self):
        return self.algorithm

    def getThumbnailUrls(self):
        return self.thumbnail_urls

    def getValue(self):
        return self.value

    def getCaption(self):
        return self.caption

    def getUser(self):
        return self.user

    def getLargeUrls(self):
        return self.large_urls

    def getMediaIds(self):
        return self.media_ids

    def getIcon(self):
        return self.icon

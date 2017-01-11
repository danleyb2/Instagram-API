from InstagramAPI.src.http.Response.Objects.User import User


class Caption(object):
    def __init__(self, data):
        self.status = None
        self.user_id = None
        self.created_at_utc = None
        self.created_at = None
        self.bit_flags = None
        self.user = None
        self.content_type = None
        self.text = None
        self.media_id = None
        self.pk = None
        self.type = None

        self.status = data['status']
        self.user_id = data['user_id']
        self.created_at_utc = data['created_at_utc']
        self.created_at = data['created_at']
        self.bit_flags = data['bit_flags']
        self.user = User(data['user'])
        self.content_type = data['content_type']
        self.text = data['text']
        self.media_id = data['media_id']
        self.pk = data['pk']
        self.type = data['type']

    def getStatus(self):
        return self.status

    def getUserId(self):
        return self.user_id

    def getCreatedAtUtc(self):
        return self.created_at_utc

    def getCreatedAt(self):
        return self.created_at

    def getBitFlags(self):
        return self.bit_flags

    def getUser(self):
        return self.user

    def getContentType(self):
        return self.content_type

    def getText(self):
        return self.text

    def getMediaId(self):
        return self.media_id

    def getUsernameId(self):
        return self.pk

    def getType(self):
        return self.type

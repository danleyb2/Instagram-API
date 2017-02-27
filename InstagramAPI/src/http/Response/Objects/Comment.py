from .User import User


class Comment(object):
    def __init__(self, commentData):
        self.status = None
        self.username_id = None
        self.created_at_utc = None
        self.created_at = None
        self.bit_flags = None
        self.user = None
        self.comment = None
        self.pk = None
        self.type = None
        self.media_id = None

        self.status = commentData['status']
        if 'user_id' in commentData and commentData['user_id']:
            self.username_id = commentData['user_id']
        self.created_at_utc = commentData['created_at_utc']
        self.created_at = commentData['created_at']
        if 'bit_flags' in commentData and commentData['bit_flags']:
            self.bit_flags = commentData['bit_flags']
        self.user = User(commentData['user'])
        self.comment = commentData['text']
        self.pk = commentData['pk']
        if 'type' in commentData and commentData['type']:
            self.type = commentData['type']
        if 'media_id' in commentData and commentData['media_id']:
            self.media_id = commentData['media_id']

    def getStatus(self):
        return self.status

    def getUsernameId(self):
        return self.username_id

    def getCreatedAtUtc(self):
        return self.created_at_utc

    def created_at(self):
        return self.created_at

    def getBitFlags(self):
        return self.bit_flags

    def getUser(self):
        return self.user

    def getComment(self):
        return self.comment

    def getCommentId(self):
        return self.pk

    def getType(self):
        return self.type

    def getMediaId(self):
        return self.media_id

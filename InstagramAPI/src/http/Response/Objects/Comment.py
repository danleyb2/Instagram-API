from User import User


class Comment(object):
    def __init__(self, commentData):
        self.username_id = None
        self.comment = None
        self.user = None

        self.username_id = commentData['user_id']
        self.comment = commentData['text']
        self.user = User(commentData['user'])

    def getUsernameId(self):
        return self.username_id

    def getComment(self):
        return self.comment

    def getUser(self):
        return self.user

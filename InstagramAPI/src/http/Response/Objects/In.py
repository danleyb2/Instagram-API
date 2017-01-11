from InstagramAPI.src.http.Response.Objects.Position import Position
from InstagramAPI.src.http.Response.Objects.User import User


class In(object):
    def __init__(self, data):
        self.position = None
        self.user = None

        self.position = Position(data['position'])
        self.user = User(data['user'])

    def getPosition(self):
        return self.position

    def getUser(self):
        return self.user

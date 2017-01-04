from Response import Response
from User import User


class FollowerResponse(Response):
    def __init__(self, response):
        self.followers = None
        if self.STATUS_OK == response['status']:
            users = []
            for user in response['users']:
                users.append(User(user))

            self.followers = users
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getFollowings(self):
        return self.followers

from InstagramAPI.src.http.Response.Objects.User import User
from Response import Response


class FollowingResponse(Response):
    def __init__(self, response):
        self.followings = None
        if self.STATUS_OK == response['status']:
            users = []
            for user in response['users']:
                users.append(User(user))
            self.followings = users
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getFollowings(self):
        return self.followings

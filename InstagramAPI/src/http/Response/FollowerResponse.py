from InstagramAPI.src.http.Response.Objects.User import User
from .Response import Response


class FollowerResponse(Response):
    def __init__(self, response):
        self.followers = None
        self.next_max_id = None

        if self.STATUS_OK == response['status']:
            users = []
            for user in response['users']:
                users.append(User(user))

            self.followers = users
            self.next_max_id = response['next_max_id'] \
                if ('next_max_id' in response and response['next_max_id']) \
                else None
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getFollowings(self):
        return self.followers

    def getNextMaxId(self):
        return self.next_max_id

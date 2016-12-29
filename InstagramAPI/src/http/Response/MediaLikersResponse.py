from InstagramAPI.src.http.Response.User import User
from Response import Response


class MediaLikersResponse(Response):
    def __init__(self, response):

        self.user_count = None
        self.likers = None

        if self.STATUS_OK == response['status']:
            users = []
            for user in response['users']:
                users.append(User(user))

            self.likers = users
            self.user_count = response['user_count']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getLikers(self):
        return self.likers

    def getLikeCounter(self):
        return self.user_count

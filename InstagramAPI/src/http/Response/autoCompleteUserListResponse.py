from InstagramAPI.src.http.Response.Objects.User import User
from .Response import Response


class autoCompleteUserListResponse(Response):

    def __init__(self, response):
        self.expires = None
        self.users = None

        if self.STATUS_OK == response['status']:
            self.expires = response['expires']
            users = []
            for user in response['users']:
                users.append(User(user))
            self.users = users
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getExpires(self):
        return self.expires

    def getUsers(self):
        return self.users

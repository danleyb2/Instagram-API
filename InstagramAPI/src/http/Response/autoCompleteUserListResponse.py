from InstagramAPI.src.http.Response.Objects.User import User
from Response import Response


class autoCompleteUserListResponse(Response):
    def __init__(self, response):
        self.expires = None
        self.users = None

        self.expires = response['expires']
        users = []
        for user in response['users']:
            users.append(User(user))

        self.users = users

    def getExpires(self):
        return self.expires

    def getUsers(self):
        return self.users

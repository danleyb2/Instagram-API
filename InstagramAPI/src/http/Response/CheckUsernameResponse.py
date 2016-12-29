from Response import Response


class CheckUsernameResponse(Response):
    def __init__(self, response):

        self.username = None
        self.available = None
        self.status = None
        self.error = False

        if self.STATUS_OK == response['status']:
            self.username = response['username']
            self.available = response['available']
            if 'error' in response:
                self.error = response['error']

        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUsername(self):

        return self.username

    def isAvailable(self):
        return self.available

    def getError(self):
        return self.error

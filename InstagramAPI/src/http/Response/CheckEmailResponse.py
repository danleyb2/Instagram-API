from Response import Response


class CheckEmailResponse(Response):
    def __init__(self, response):

        self.username = None
        self.confirmed = None
        self.status = None
        self.valid = None
        self.username_suggestions = None

        if self.STATUS_OK == response['status']:
            self.confirmed = response['confirmed']
            self.available = response['available']
            self.valid = response['valid']
            if 'username_suggestions' in response:
                self.username_suggestions = response['username_suggestions']

        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def isConfirmed(self):
        return self.confirmed

    def isAvailable(self):
        return self.available

    def isValid(self):
        return self.valid

    def getUsernameSuggestions(self):
        return self.username_suggestions

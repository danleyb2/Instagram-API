from Response import Response


class UsernameSuggestionsResponse(Response):
    def __init__(self, response):
        self.username_suggestions = None
        if self.STATUS_OK == response['status']:
            if 'username_suggestions' in response:
                self.username_suggestions = response['username_suggestions']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUsernameSuggestions(self):
        return self.username_suggestions

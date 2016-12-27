from Response import Response


class ChallengeResponse(Response):
    def __init__(self, response):

        if self.STATUS_OK == response['status']:
            pass
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

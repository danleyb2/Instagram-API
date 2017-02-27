from .Response import Response


class LogoutResponse(Response):
    def __init__(self, response):

        if self.STATUS_OK == response['status']:
            pass
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

from .Response import Response


class MegaphoneLogResponse(Response):
    def __init__(self, response):
        self.success = None

        if self.STATUS_OK == response['status']:
            self.success = response['success']
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def isSuccess(self):
        return self.success

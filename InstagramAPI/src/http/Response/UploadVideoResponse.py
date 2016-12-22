from Response import Response


class UploadVideoResponse(Response):
    def __init__(self, response):
        self.upload_id = None

        if self.STATUS_OK == response['status']:
            self.upload_id = response['upload_id']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUploadId(self):
        return self.upload_id

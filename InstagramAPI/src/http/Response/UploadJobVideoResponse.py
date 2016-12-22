from Response import Response


class UploadJobVideoResponse(Response):
    def __init__(self, response):
        self.upload_id = None
        self.video_upload_urls = None

        if self.STATUS_OK == response['status']:
            self.upload_id = response['upload_id']
            self.video_upload_urls = response['video_upload_urls']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUploadId(self):
        return self.upload_id

    def getVideoUploadUrls(self):
        return self.video_upload_urls

    def getVideoUploadUrl(self):
        return self.getVideoUploadUrls()[3]['url']

    def getVideoUploadJob(self):
        return self.getVideoUploadUrls()[3]['job']

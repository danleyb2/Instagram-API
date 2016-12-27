from Response import Response


class ConfigureResponse(Response):
    def __init__(self, response):
        self.upload_id = None
        self.media_id = None
        self.image_url = None
        self.media_code = None

        if self.STATUS_OK == response['status']:
            self.upload_id = response['upload_id']
            self.media_id = response['media']['id']
            self.image_url = response['media']['image_versions2']['candidates']['0']['url']
            self.media_code = response['media']['code']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getUploadId(self):
        return self.upload_id

    def getMediaId(self):
        return self.media_id

    def getImageUrl(self):
        return self.image_url

    def getMediaCode(self):
        return self.media_code

    def getMediaUrl(self):
        return 'https://www.instagram.com/p/' + self.getMediaCode() + '/'

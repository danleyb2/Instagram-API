from .Response import Response


class RecentRecipientsResponse(Response):
    def __init__(self, response):
        self.expiration_interval = None
        self.recent_recipients = None

        if self.STATUS_OK == response['status']:
            self.expiration_interval = response['expiration_interval']
            self.recent_recipients = response['recent_recipients']
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getExpirationInterval(self):
        return self.expiration_interval

    def getRecentRecipients(self):
        return self.recent_recipients

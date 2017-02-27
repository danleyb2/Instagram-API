from .Response import Response


class RankedRecipientsResponse(Response):
    def __init__(self, response):
        self.expires = None
        self.ranked_recipients = None

        if self.STATUS_OK == response['status']:
            self.expires = response['expires']
            self.ranked_recipients = response['ranked_recipients']
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getExpires(self):
        return self.expires

    def getRankedRecipients(self):
        return self.ranked_recipients

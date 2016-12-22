class Response(object):
    STATUS_OK = "ok"
    STATUS_FAIL = "fail"

    def __init__(self):
        self.status = None
        self.message = None

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setMessage(self, message):
        self.message = message

    def getMessage(self):
        return self.message

    def isOk(self):
        return self.getStatus() == Response.STATUS_OK

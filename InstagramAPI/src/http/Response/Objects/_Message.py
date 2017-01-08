class _Message(object):
    def __init__(self, data):
        self.key = None
        self.time = None

        self.key = data['key']
        self.time = data['time']

    def getKey(self):
        return self.key

    def getTime(self):
        return self.time

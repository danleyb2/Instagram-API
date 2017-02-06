class Param(object):
    def __init__(self, data):
        self.name = None
        self.value = None

        self.name = data['name']
        self.value = data['value']

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

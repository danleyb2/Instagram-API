class Position(object):
    def __init__(self, data):
        self.pos1 = None
        self.pos2 = None

        self.pos1 = data[0]
        self.pos2 = data[1]

    def getPos1(self):
        return self.pos1

    def getPos2(self):
        return self.pos2

class Tray(object):
    def __init__(self, items, user, can_reply, expiring_at):
        self.items = None
        self.user = None
        self.can_reply = None
        self.expiring_at = None

        self.items = items
        self.user = user
        self.can_reply = can_reply
        self.expiring_at = expiring_at

    def getItems(self):
        return self.items

    def getUsers(self):
        return self.users

    def canReply(self):
        return self.can_reply

    def getExpiringAt(self):
        return self.expiring_at

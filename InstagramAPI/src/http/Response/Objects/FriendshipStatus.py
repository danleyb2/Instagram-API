class FriendshipStatus(object):
    def __init__(self, data):
        self.following = None
        self.incoming_request = None
        self.outgoing_request = None
        self.is_private = None

        self.following = data['following']
        if 'source_token' in data:
            self.incoming_request = data['incoming_request']
        if 'source_token' in data:
            self.outgoing_request = data['outgoing_request']
        if 'is_private' in data:
            self.is_private = data['is_private']

    def getFollowing(self):
        return self.following

    def getIncomingRequest(self):
        return self.incoming_request

    def getOutgoingRequest(self):
        return self.outgoing_request

    def isPrivate(self):
        return self.is_private

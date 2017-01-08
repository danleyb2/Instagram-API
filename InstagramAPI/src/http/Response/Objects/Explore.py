class Explore(object):
    def __init__(self, data):
        self.explanation = None
        self.actor_id = None
        self.source_token = None

        self.explanation = data['explanation']
        self.actor_id = data['actor_id']
        self.source_token = data['source_token']

    def getExplanation(self):
        return self.explanation

    def getActorId(self):
        return self.actor_id

    def getSourceToken(self):
        return self.source_token

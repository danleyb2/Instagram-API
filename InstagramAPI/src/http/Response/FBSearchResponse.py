from .Response import Response


class FBSearchResponse(Response):
    def __init__(self):
        self.has_more = None
        self.hashtags = None
        self.users = None
        self.places = None

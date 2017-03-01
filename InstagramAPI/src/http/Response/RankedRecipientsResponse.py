from .Response import Response


class RankedRecipientsResponse(Response):
    def __init__(self):
        self.expires = None
        self.ranked_recipients = None

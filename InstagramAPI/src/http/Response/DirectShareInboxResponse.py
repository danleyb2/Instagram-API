from .Response import Response


class DirectShareInboxResponse(Response):
    def __init__(self):
        self.shares = None
        self.max_id = None
        self.new_shares = None
        self.patches = None
        self.last_counted_at = None
        self.new_shares_info = None

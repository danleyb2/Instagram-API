from .Response import Response


class FollowingRecentActivityResponse(Response):
    def __init__(self):
        self.stories = None
        self.next_max_id = None

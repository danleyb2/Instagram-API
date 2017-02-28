from .Response import Response


class UsertagsResponse(Response):
    def __init__(self):
        self.num_results = None
        self.auto_load_more_enabled = None
        self.items = None
        self.more_available = None
        self.next_max_id = None
        self.total_count = None
        self.requires_review = None
        self.new_photos = None

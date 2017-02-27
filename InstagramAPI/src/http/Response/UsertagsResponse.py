from InstagramAPI.src.http.Response.Objects.Item import Item
from .Response import Response


class UsertagsResponse(Response):
    def __init__(self, response):

        self.num_results = None
        self.auto_load_more_enabled = None
        self.items = None
        self.more_available = None
        self.next_max_id = None
        self.total_count = None
        self.requires_review = None
        self.new_photos = None

        if self.STATUS_OK == response['status']:
            self.num_results = response['num_results']
            self.auto_load_more_enabled = response['auto_load_more_enabled']
            items = []
            for item in response['items']:
                items.append(Item(item))

            self.items = items
            self.more_available = response['more_available']
            self.next_max_id = response['next_max_id']
            self.total_count = response['total_count']
            self.requires_review = response['requires_review']
            self.new_photos = response['new_photos']
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

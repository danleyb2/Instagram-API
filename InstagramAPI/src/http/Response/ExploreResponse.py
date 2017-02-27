from InstagramAPI.src.http.Response.Objects.Item import Item
from .Response import Response


class ExploreResponse(Response):
    def __init__(self, response):
        self.num_results = None
        self.auto_load_more_enabled = None
        self.items = None
        self.more_available = None
        self.next_max_id = None
        self.max_id = None

        if self.STATUS_OK == response['status']:
            self.num_results = response['num_results']
            self.auto_load_more_enabled = response['auto_load_more_enabled']
            self.more_available = response['more_available']
            self.next_max_id = response['next_max_id']
            self.max_id = response['max_id']
            items = []
            for item in response['items']:
                if 'media' in item and item['media']:
                    items.append(Item(item['media']))

            self.items = items
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getExpires(self):
        return self.expires

    def getUsers(self):
        return self.users

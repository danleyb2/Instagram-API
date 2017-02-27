from InstagramAPI.src.http.Response.Objects.Item import Item
from .Response import Response


class UserFeedResponse(Response):
    def __init__(self, response):
        self.num_results = None
        self.auto_load_more_enabled = None
        self.items = None
        self.more_available = None
        self.next_max_id = null = None

        if self.STATUS_OK == response['status']:
            if 'next_max_id' in response:
                self.next_max_id = response['next_max_id']

            self.num_results = response['num_results']
            self.auto_load_more_enabled = response['auto_load_more_enabled']
            items = []
            for item in response['items']:
                items.append(Item(item))
            self.items = items
            self.more_available = response['more_available']
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getNumResults(self):
        return self.num_results

    def getAutoLoadMoreEnabled(self):
        return self.auto_load_more_enabled

    def getItems(self):
        return self.items

    def moreAvailable(self):
        return self.more_available

    def getNextMaxId(self):
        return self.next_max_id

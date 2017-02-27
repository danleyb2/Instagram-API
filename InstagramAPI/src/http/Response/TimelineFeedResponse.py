from InstagramAPI.src.http.Response.Objects.FeedAysf import FeedAysf
from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Objects._Message import _Message
from .Response import Response


class TimelineFeedResponse(Response):
    def __init__(self, response):

        self.num_results = None
        self.is_direct_v2_enabled = None
        self.auto_load_more_enabled = None
        self.more_available = None
        self.next_max_id = None
        self._messages = None
        self.feed_items = None
        self.megaphone = None

        if self.STATUS_OK == response['status']:
            self.num_results = response['num_results']
            self.is_direct_v2_enabled = response['is_direct_v2_enabled']
            self.auto_load_more_enabled = response['auto_load_more_enabled']
            self.more_available = response['more_available']
            self.next_max_id = response['next_max_id']
            messages = []
            if '_messages' in response and len(response['_messages']):
                for message in response['_messages']:
                    messages.append(_Message(message))

            self._messages = messages
            items = []
            if 'feed_items' in response and len(response['feed_items']):
                for item in response['feed_items']:
                    if 'media_or_ad' in item and item['media_or_ad']:
                        items.append(Item(item['media_or_ad']))

            self.feed_items = items
            self.megaphone = FeedAysf(response['megaphone']['feed_aysf']) if \
                ('megaphone' in response and 'feed_aysf' in response['megaphone']) else None

        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getNumResults(self):
        return self.num_results

    def isDirectV2Enabled(self):
        return self.is_direct_v2_enabled

    def autoLoadMoreEnabled(self):
        return self.auto_load_more_enabled

    def moreAvailable(self):
        return self.more_available

    def getNextMaxId(self):
        return self.next_max_id

    def getExternalId(self):
        return self.external_id

    def getMessages(self):
        return self._messages

    def getFeedItems(self):
        return self.feed_items

    def getMegaphone(self):
        return self.megaphone

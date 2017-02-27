from InstagramAPI.src.http.Response.Objects.Item import Item
from .Response import Response


class MediaCommentsResponse(Response):
    def __init__(self, response):
        self.item = None

        if self.STATUS_OK == response['status']:
            if 'media' in response and response['media']:
                self.item = Item(response['media'])
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getItem(self):
        return self.taken_at  # Unresolved reference attribute

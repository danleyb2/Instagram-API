from InstagramAPI.src.http.Response.Objects.Item import Item
from InstagramAPI.src.http.Response.Objects.Tray import Tray
from Response import Response


class ReelsTrayFeedResponse(Response):
    def __init__(self, response):

        self.trays = None

        if self.STATUS_OK == response['status']:
            trays = []
            if 'tray' in response and len(response['tray']):
                for tray in response['tray']:
                    items = []
                    if 'items' in tray and len(tray['items']):
                        for item in tray['items']:
                            items.append(Item(item))

                    trays.append(Tray(items, tray['user'], tray['can_reply'], tray['expiring_at']))

            self.trays = trays
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getTrays(self):
        return self.trays

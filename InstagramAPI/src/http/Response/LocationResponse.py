from Response import Response


class LocationResponse(Response):
    def __init__(self, response):
        self.venues = None

        if self.STATUS_OK == response['status']:
            locations = []
            for location in response['venues']:
                locations.append(Location(location))

            self.venues = locations
        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])

    def getVenues(self):
        return self.venues

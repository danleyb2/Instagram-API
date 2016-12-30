class Location(object):
    def __init__(self, location):
        self.name = None
        self.external_id_source = None
        self.address = None
        self.lat = None
        self.lng = None
        self.external_id = None

        self.name = location['name']
        self.external_id_source = location['external_id_source']
        self.address = location['address']
        self.lat = location['lat']
        self.lng = location['lng']
        self.external_id = location['external_id']

    def getName(self):
        return self.name

    def getExternalIdSource(self):
        return self.external_id_source

    def getAddress(self):
        return self.address

    def getLatitude(self):
        return self.lat

    def getLongitude(self):
        return self.lng

    def getExternalId(self):
        return self.external_id

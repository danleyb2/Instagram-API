from InstagramAPI.src.http.Response.Objects.In import In


class Usertag(object):
    def __init__(self, data):
        self._in = None
        self.photo_of_you = None

        ins = []
        for _in in data['in']:
            _in.append(In(_in))  # todo possible bug `_in.append`

        self._in = ins

    def getIn(self):
        return self._in

    def getPhotoOfYou(self):
        return self.photo_of_you

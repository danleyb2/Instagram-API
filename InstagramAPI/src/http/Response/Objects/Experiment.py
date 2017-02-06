from InstagramAPI.src.http.Response.Objects.Param import Param


class Experiment(object):
    def __init__(self, data):
        self.params = None
        self.group = None
        self.name = None

        params = []
        for param in data['params']:
            params.append(Param(param))

        self.params = params
        self.group = data['group']
        self.name = data['name']

    def getParams(self):
        return self.params

    def getGroup(self):
        return self.group

    def getName(self):
        return self.name

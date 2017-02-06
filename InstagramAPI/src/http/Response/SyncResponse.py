from InstagramAPI.src.http.Response import Response
from InstagramAPI.src.http.Response.Objects.Experiment import Experiment


class SyncResponse(Response):
    def __init__(self, response):
        self.experiments = None

        if self.STATUS_OK == response['status']:
            experiments = []
            for experiment in response['experiments']:
                experiments.append(Experiment(experiment))
            self.experiments = experiments
        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getExperiments(self):
        return self.experiments

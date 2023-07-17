import numpy as np
from similarity_ts.metrics.metric import Metric


class EuclideanDistance(Metric):

    def __init__(self):
        super().__init__()
        self.name = 'eu'

    def compute(self, ts1, ts2):
        metric_result = {'Multivariate': self.__eu(ts1, ts2)}
        return metric_result

    def compute_distance(self, ts1, ts2):
        return self.__eu(ts1, ts2)

    def __eu(self, ts1, ts2):
        return np.linalg.norm(ts1 - ts2)

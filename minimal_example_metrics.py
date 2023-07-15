import numpy as np
from similarity_ts.similarity_ts import SimilarityTs

ts1 = np.random.rand(200, 2)
ts2s = np.random.rand(5, 100, 2)
similarity_ts = SimilarityTs(ts1, ts2s)
for ts2_name, metric_name, computed_metric in similarity_ts.get_metric_computer():
    print(f'{ts2_name}. {metric_name}: {computed_metric}')
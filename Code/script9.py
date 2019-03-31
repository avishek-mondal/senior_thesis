import sys
import json
import sys
import numpy as np

sys.path.append('../..')

import risk_similarity_calc
import ASClusteringDeNasa_080119
import security_calc_09012019

ASClusteringDeNasa_080119.clustering(10,'risk_similarity_metric')
security_calc_09012019.security_calc('10_risk_similarity_metric','risk_similarity_metric_10')
ASClusteringDeNasa_080119.clustering(15,'risk_similarity_metric')
security_calc_09012019.security_calc('15_risk_similarity_metric','risk_similarity_metric_15')

ASClusteringDeNasa_080119.clustering(20,'risk_similarity_metric')
security_calc_09012019.security_calc('20_risk_similarity_metric','risk_similarity_metric_20')

ASClusteringDeNasa_080119.clustering(25,'risk_similarity_metric')
security_calc_09012019.security_calc('25_risk_similarity_metric','risk_similarity_metric_25')

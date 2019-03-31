import sys
import json
import sys
import numpy as np

sys.path.append('../..')

import risk_similarity_calc
import ASClusteringDeNasa_100119
import security_calc_09012019

ASClusteringDeNasa_100119.clustering(10,'')
security_calc_09012019.security_calc('10__10012019', 'original')

ASClusteringDeNasa_100119.clustering(20,'')
security_calc_09012019.security_calc('20__10012019', '20_original')

import sys
import json
import sys
import numpy as np

sys.path.append('../..')

import ASClusteringDeNasa_010219
import calculate_similarity
import whisker_plot_self_similarity_030219
import calculate_increase_in_risk


date = '050219'
nsf = "../Data/2016-10-01-00-00-00-network_state"
num_clusters = '10'
similarity_index_name = 'jaccard_new_test'

ASSimilarityFileName = calculate_similarity.jaccard(date,similarity_index_name, nsf)
similarityClusterFileName = ASClusteringDeNasa_010219.clustering_test(num_clusters, similarity_index_name, date, ASSimilarityFileName)
calculate_increase_in_risk.security_calc(similarityClusterFileName, num_clusters, similarity_index_name, date)


whisker_plot_self_similarity_030219.whisker_plot(similarityClusterFileName)

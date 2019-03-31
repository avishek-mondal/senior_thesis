import sys
import json
import sys
import numpy as np

sys.path.append('../..')

import ASClustering
import calculate_similarity
import whisker_plot_self_similarity_030219
import calculate_increase_in_risk


date = '210319'
nsf = "../Data/2016-10-01-00-00-00-network_state"
num_clusters = '10'
similarity_index_name = 'jaccard'

# ASSimilarityFileName = "../Data/ASSimilarityFile_jaccard_080319.json"
ASSimilarityFileName = calculate_similarity.jaccard(date,similarity_index_name, nsf)
similarityClusterFileName = ASClustering.clustering(num_clusters, similarity_index_name, date, ASSimilarityFileName)
calculate_increase_in_risk.security_calc(similarityClusterFileName, num_clusters, similarity_index_name, date)


whisker_plot_self_similarity_030219.whisker_plot(similarityClusterFileName)

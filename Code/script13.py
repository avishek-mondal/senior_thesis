import sys
import json
import sys
import numpy as np

sys.path.append('../..')

import ASClustering
import calculate_similarity
import whisker_plot_self_similarity_030219
import calculate_increase_in_risk


date = '270319'
nsf = "../Data/2016-10-01-00-00-00-network_state"
num_clusters = '10'
similarity_index_name = 'jaccard'
guard_selection_probs_file_name = '../Data/guard_selection_probs.json'

ASSimilarityFileName = "../Data/ASSimilarityFile_jaccard_210319.json"
# ASSimilarityFileName = calculate_similarity.jaccard(date,similarity_index_name, nsf)
similarityClusterFileName = ASClustering.clustering_risk_accounted(num_clusters, similarity_index_name, date, \
                                                                        ASSimilarityFileName, \
                                                                        guard_selection_probs_file_name)
calculate_increase_in_risk.security_calc(similarityClusterFileName, num_clusters, similarity_index_name, date)


whisker_plot_self_similarity_030219.whisker_plot(similarityClusterFileName)

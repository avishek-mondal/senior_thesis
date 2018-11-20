import sys
import ASWeightEuclideanSimilarity
import  ASClusteringDeNasa


ASWeightEuclideanSimilarity.weight_comparison("../Data/guard_selection_probs.json","Euclidean")
ASClusteringDeNasa.clustering('10','')

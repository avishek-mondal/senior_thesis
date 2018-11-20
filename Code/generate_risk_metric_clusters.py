import sys
import risk_similarity_calc
import  ASClusteringDeNasa

#generates clusters
risk_similarity_calc.calculate_risk_similarity("../Data/guard_selection_probs.json","RiskMetric")
ASClusteringDeNasa.clustering('10','RiskMetric')

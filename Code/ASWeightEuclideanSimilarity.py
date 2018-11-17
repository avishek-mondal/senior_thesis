'''
ASWeightEuclideanSimilarity.py
Modified by Avishek, to use DeNASA parameters as input
Author: Eric Ham
Works with Python 3
Last Updated: 11/1/18
Original Description: Takes CounterRaptorWeights.json/CounterRaptorWeightVanilla.json/CounterRaptorWeightNoBW.json as input and outputs a file
which shows the similarity between each pair of ASes based on euclidian distance.
Input: CounterRaptorWeights.json
Output: ASSimilarityFile.json
Command Line: Input (CounterRaptorWeights.json etc)
Running: python3 ASWeightComparison.py

'''

import json
import math
from copy import deepcopy
import sys
#outputChar used with SimilarityAndHijackResilienceOverTime.py to create differently named files for each iteration
def weight_comparison(inputVal,outputChar):

	as_to_as_similarity = dict()
	with open(inputVal) as data_file:
		data = json.load(data_file)
		max_similarity = 0
		# Here we get similarities for each AS to every other AS
		for key1, values1 in data.items():
			key1_weights = deepcopy(values1)
			as_to_as_similarity[key1] = {}
			for key, values in data.items():
				weightSim = 0
				to_guard_weights = deepcopy(values)
				for ip in key1_weights:
					weightSim += (key1_weights[ip]-to_guard_weights[ip])*(key1_weights[ip]-to_guard_weights[ip])
				weightSim = math.sqrt(weightSim)
				#calculate max value
				if weightSim > max_similarity:
					max_similarity = weightSim
				as_to_as_similarity[key1][key] = weightSim
		#normalize and subtract from 1 so the higher similarities signify greater similarity
		for AS in as_to_as_similarity:
			for AS2 in as_to_as_similarity[AS]:
				if max_similarity == 0:
					as_to_as_similarity[AS][AS2] = 0
				else:
					as_to_as_similarity[AS][AS2] = 1 - (as_to_as_similarity[AS][AS2]/max_similarity)



	data_file.close()
	file_out = open('../Data/ASSimilarityFile' + str(outputChar) + '.json', 'w+')
	json.dump(as_to_as_similarity, file_out)
	file_out.close()

if __name__ == '__main__':
	weight_comparison(sys.argv[1],sys.argv[2])

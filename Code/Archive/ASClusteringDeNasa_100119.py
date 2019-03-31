'''
ASClustering.py
Description: Clusters ASes by similarity so that a user can more easily choose an alias AS using balanced algorithm.
Input: number of clusters or all to create sets of 5, 10, 20, 100 clusters.
Output: similarity_clusters_[num].json
Command Line: Input
Running: python3 ASClustering.py [number of clusters]

'''
import json
import math
from copy import deepcopy
import random
import sys

#holds a list of ases that are still unchosen
as_list = {}

#holds a list of all ASes
as_listCopy = {}

# Finds the non-rep AS that is most similar to the given representative AS.
def mostSimilarAS(rep_AS):
	highest_similarity_value = 0												#
	new_cluster_AS = ''
	equals_rep = 0
	#at this point the reps should not be in as_list.
	for AS in as_list:
		if as_listCopy[AS][rep_AS] > highest_similarity_value:						#
			new_cluster_AS = AS
			highest_similarity_value = as_listCopy[AS][rep_AS]

	#if highest similarity is still 0, then randomly choose new_cluster_AS
	if highest_similarity_value == 0:
		new_cluster_AS, _ = random.choice(list(as_list.items()))
	#remove member AS so don't consider again in future
	as_list.pop(new_cluster_AS)
	return new_cluster_AS, highest_similarity_value

#Given a random cluster representative, and a number of desired clusters, finds num_clusters - 1 representatives for the remaining clusters that are
#maximally dissimilar to the current cluster representatives.
def clusterReps(num_clusters, clusterRepArray):
	for i in range(num_clusters-1):
		new_cluster_rep = 0
		similarity_to_be_smaller_than = len(clusterRepArray) #1*num_clusters
		for AS in as_list:
			similarity = 0
			for rep in clusterRepArray:
				similarity += as_listCopy[AS][rep]
			if similarity <= similarity_to_be_smaller_than:
				similarity_to_be_smaller_than = similarity
				new_cluster_rep = AS
		clusterRepArray[new_cluster_rep] = as_listCopy[new_cluster_rep]
		as_list.pop(new_cluster_rep)

#Clustering algorithm
#inputChar used with SimilarityAndHijackResilienceOverTime.py to create differently named files for each iteration
def clustering(sizes, inputChar):
	cluster_sizes = []
	#facilitates creating diff numbers of clusters for testing.
	if sizes == 'all':
		cluster_sizes.append(5)
		cluster_sizes.append(10)
		cluster_sizes.append(20)
		cluster_sizes.append(50)
		cluster_sizes.append(100)
	else:
		cluster_sizes.append(int(sizes))
	failure = []
	fail_cluster = 0
	for index in range(len(cluster_sizes)):
		failure.append(0)

	for num_clusters in cluster_sizes:
		#holds the cluster representatives and their connections to every AS
		cluster_reps_array = {}


		#contains all cluster and their cluster members and the similarities to each member
		cluster_array = {}
		with open("../Data/ASSimilarityFile" + str(inputChar) + ".json") as data_file:
			data = json.load(data_file)
			for key, values in data.items():
				as_list[key] = values
				as_listCopy[key] = values
			#pick a random first cluster representative
			first_AS_cluster_rep, first_AS_cluster_relationships = random.choice(list(data.items()))

			cluster_reps_array[first_AS_cluster_rep] = first_AS_cluster_relationships
			as_list.pop(first_AS_cluster_rep)

			#choose remaining cluster representatives so that they are most dissimilar to the initial representative.
			clusterReps(num_clusters, cluster_reps_array)

			#refill as_list since you popped all of its memebrs in clusterReps
			cluster_array = {}
			for rep_AS in cluster_reps_array:
				cluster_array[rep_AS] = dict()

			rounds = 0
			max_rounds = 100
			while rounds < max_rounds:
				#go through every other AS (excluding reps)
				#length_observed_ASes = len(as_listCopy) - num_clusters
				# after first round need to remove cluster reps in here because not calling clusterReps

				for rep_AS in cluster_reps_array:
					if rep_AS in as_list:
						as_list.pop(rep_AS)


				while len(as_list) != 0:
					for AS in cluster_reps_array:
						#find themost similar AS and the similarity value for the given representative
						print('AS is :',AS)
						new_cluster_AS, highest_similarity = mostSimilarAS(AS)
						#assign the most similar AS to that cluster
						cluster_array[AS][new_cluster_AS] = highest_similarity
						#length_observed_ASes -= 1
						if len(as_list) == 0:
							break

				#signifies completition of one round
				rounds+=1
				print('^ROUND # ' + str(rounds) + ': \n')
				if rounds >= max_rounds:
					break

				#number of cluster rep changes
				numChanges = 0
				#ne rep AS value
				new_rep = 0
				#for finding smallest avg similarity value from a given AS to all other ASes in clsuter
				smallest_similarity_sum = 0
				#temporary cluster array
				new_cluster_array = {}
				#temporary array of cluster representatives
				new_cluster_reps_array = {}

				for rep in cluster_array:
					#signifies the avg similarity value from rep to its members
					rep_similarity_sum = 0
					#signifies if the cluster changed
					changed = 0
					#calculate rep_similarity_sum
					for member in cluster_array[rep]:
						rep_similarity_sum += cluster_array[rep][member]
					if rep_similarity_sum !=0:
						rep_similarity_sum /= len(cluster_array[rep])
					most_similar_sum = rep_similarity_sum
					#find avg simmilarity values for every member in a cluster to all other members (including representative)
					for member in cluster_array[rep]:
						similarity_sum = 0
						for member2 in cluster_array[rep]:
							if member == member2:
								continue
							similarity_sum += as_listCopy[member][member2]
						similarity_sum += as_listCopy[member][rep]
						if similarity_sum !=0:
							similarity_sum /= len(cluster_array[rep])
						# if the average similarity of one member is less (it is more similar to other values) than that of the rep, make it the cluster rep
						if similarity_sum > most_similar_sum:
							most_similar_sum = similarity_sum
							new_rep = member
							changed = 1

					# if cluster representative changed and fewer than max_rounds assignment rounds, redo cluster assignment. with new representatives.
					if changed != 0:
						print('new rep' + str(new_rep))
						new_cluster_reps_array[new_rep] = as_listCopy[new_rep]
						new_cluster_array[new_rep] = dict()
						numChanges+= 1
						changed = 0
					else:
						print('no change in cluster' + str(rep))
						new_cluster_reps_array[rep] = as_listCopy[rep]
						new_cluster_array[rep] = dict()

				if numChanges == 0:
					#you are done!
					print('no change')
					break
				else:
					#copy values back into original arrays from temporary arrays
					for key in as_listCopy:
						as_list[key] = as_listCopy[key]
					cluster_array = deepcopy(new_cluster_array)
					cluster_reps_array = deepcopy(new_cluster_reps_array)

		#cluster check
		list_of_clusters = {}
		i = 0
		for key in cluster_array:
			list_of_clusters[i] = []
			list_of_clusters[i].append(key)
			for member in cluster_array[key]:
				list_of_clusters[i].append(member)
			i+=1

		for index_1 in range(len(list_of_clusters)):
			for index_2 in range(len(list_of_clusters)):
				if index_2 <= index_1:
					continue
				for member_1 in list_of_clusters[index_1]:
					for member_2 in list_of_clusters[index_2]:
						if member_1 == member_2:
							failure.remove(0)
							failure.append(1)
							fail_cluster = num_clusters

		data_file.close()
		file_out = open('../Data/similarity_clusters_' + str(num_clusters) + '_'+ str(inputChar)+'_10012019.json', 'w+')
		json.dump(cluster_array, file_out)
		file_out.close()
	#Tells you if clustering failed
	for val in failure:
		if val == 1:
			print('Clustering with num_clusters: ' + str(fail_cluster) + ' Failed')

if __name__ == '__main__':
	clustering(10,'jaccard')

import json
import numpy as np
import random
from copy import deepcopy


# rep_AS is a string, AS_list is a dict, not a dict of dicts!
def most_similar_AS(rep_AS, AS_list, member_AS_list):
    # remove itself from the AS_list
    self_val = AS_list.pop(rep_AS)
    vals = [(AS_list[AS], AS) for AS in member_AS_list]
    vals = sorted(vals, reverse=True)
    most_similar_AS = vals[0][1]
    # add self back
    AS_list.update({rep_AS: self_val})
    # return back only one AS
    return most_similar_AS


# method to get num_clusters number of dissimilar ASes to the first random AS
# chosen randomly. returns a list
def choose_dissimilar_cluster_representatives(num_clusters, first_AS_cluster_rep, \
                                              first_AS_cluster_relationships):
    cluster_representatives = [first_AS_cluster_rep]
    # extract the most dissimilar values
    cluster_representatives.extend(sorted(first_AS_cluster_relationships, \
                                          key=first_AS_cluster_relationships.get, \
                                          reverse=False)[:int(num_clusters) - 1])

    return cluster_representatives


# # return the AS with the most similar AS to the AS passed
# def most_similar_AS(AS, AS_similarity_data):
#     # return AS with the maximum similarity value
#     return max(AS_similarity_data[AS], key = AS_similarity_data[AS].get)


# 3a) Assign most similar AS to first cluster representative and so on
def sequential_assignment(cluster_representatives, AS_similarity_data):
    all_ASes_list = list(AS_similarity_data.keys())
    member_AS_list = [AS for AS in all_ASes_list if AS not in cluster_representatives]
    AS_similarity_data_copy = deepcopy(AS_similarity_data)

    # going to return dictionary of dictionaries
    clusters = {}

    # initialise the cluster return dictionary of dictionaries
    # this is so that in the next loop we can use update
    for cluster_representative in cluster_representatives:
        clusters[cluster_representative] = {}

    # go ahead and assign, until no member ASes remain
    while member_AS_list:
        for cluster_representative in cluster_representatives:
            mostSimilarAS = most_similar_AS(cluster_representative, \
                                            AS_similarity_data_copy[cluster_representative], \
                                            member_AS_list)

            # if it is another cluster representative, then ignore, otherwise,
            # store is in the clusters
            if mostSimilarAS not in cluster_representatives:
                clusters[cluster_representative].update( \
                    {mostSimilarAS: \
                         AS_similarity_data_copy[cluster_representative][mostSimilarAS]})
                member_AS_list.remove(mostSimilarAS)

            # no matter what, just pop whatever the most similar AS was
            AS_similarity_data_copy[cluster_representative].pop(mostSimilarAS)
            if not member_AS_list:
                break

    # print("leaving sequential assignment")
    # print("cluster representatives: ", cluster_representatives)
    # print(len(cluster_representatives))
    return clusters


def generate_count_dict(usability_table, all_ASes_list):
    count_dict = {}
    for AS in all_ASes_list:
        d = {(i, j): v for (i, j), v in usability_table.items() if v == True and i == AS}
        count_dict[AS] = len(d)
    return count_dict


def choose_most_restricitve_AS(inp_dict, count_dict):
    member_ASes = list(inp_dict.keys())
    min_count = 3000

    for member_AS in member_ASes:
        if count_dict[member_AS] <= min_count:
            ret_AS = member_AS
            min_count = count_dict[member_AS]

    return ret_AS


def clustering_most_restrictive_guard(num_clusters, similarity_index_name, date, AS_similarity_file_name):
    usability_table = np.load('../Data/usability_table.npy').item()

    with open(AS_similarity_file_name) as data_file:
        AS_similarity_data = json.load(data_file)

    all_ASes_list = list(AS_similarity_data.keys())

    # generate the dictionary that shows the number of guards that each AS can usable
    # generated in generate_count_dict.py file
    # count_dict = generate_count_dict(usability_table, all_ASes_list)
    with open('../Data/count_dict.json') as data_file:
        count_dict = json.load(data_file)

    # 1) choose a random AS
    first_AS_cluster_rep, first_AS_cluster_relationships = random.choice(list(AS_similarity_data.items()))

    # 2) choose k most dissimilar ASes to this AS to be cluster cluster_representatives
    cluster_representatives = choose_dissimilar_cluster_representatives(num_clusters, \
                                                                        first_AS_cluster_rep, \
                                                                        first_AS_cluster_relationships)

    # print(cluster_representatives)
    # 3) all other ASes are assigned to one of these cluster representatives. Assign member ASes
    # sequentially to the cluster representatives

    # 3a) Assign most similar AS to first cluster representative and so on
    clusters = sequential_assignment(cluster_representatives, AS_similarity_data)

    # 4) Within each cluster, if there's an AS that the member ASes are more similar to,
    # assign that as a cluster representative. Repeat for max_number_of_rounds
    max_number_of_rounds = 1000
    round_number = 0

    # 4a) sum up the value of similarity in each cluster and divide by total number of
    #     ASes in the cluster to compare the similarity
    while round_number < max_number_of_rounds:

        # maintain a flag to keep track of any changes to the round
        round_change_flag = False

        # loop through each cluster representative
        if cluster_representatives:
            new_cluster_representatives = []
            new_cluster_representatives = deepcopy(cluster_representatives)
            for cluster_representative in cluster_representatives:

                if (len(clusters[cluster_representative]) != 0):
                    curr_avg_sim_val = sum(clusters[cluster_representative].values()) / \
                                       len(clusters[cluster_representative])
                else:
                    curr_avg_sim_val = 0

                member_ASes = list(clusters[cluster_representative].keys())
                change_flag = False;

                # compare avg_sim_val to curr_avg_sim_val to update
                for member_AS in member_ASes:
                    # start by adding the similarity val of the cluster representatives
                    # to the member AS under consideration, because it could be a member
                    # later
                    avg_sim_val = AS_similarity_data[cluster_representative][member_AS]
                    # loop through the other member ASes and add the similarity values
                    for member_AS_inner in member_ASes:
                        avg_sim_val += AS_similarity_data[member_AS][member_AS_inner]

                    # subtract the value self similarity value because we have double
                    # counted the member AS itself
                    avg_sim_val -= 1
                    avg_sim_val = avg_sim_val / (len(clusters[cluster_representative]))

                    # if avg_sim_val is > curr_avg_sim_val, remove the current cluster
                    # rep and make the member AS the cluster representative

                    if avg_sim_val > curr_avg_sim_val:
                        # print('old sim val: ', curr_avg_sim_val, ' new sim val: ', avg_sim_val)
                        # print("old cluster_representative: ", cluster_representative)
                        # new_cluster_representative = member_AS
                        # print("new_cluster_representative: ", new_cluster_representative)
                        curr_avg_sim_val = avg_sim_val
                        change_flag = True
                        round_change_flag = True

                if change_flag:
                    # print("entering change flag")
                    new_cluster_representative = choose_most_restricitve_AS(clusters[cluster_representative], \
                                                                            count_dict)
                    new_cluster_representatives.remove(cluster_representative)
                    new_cluster_representatives.append(new_cluster_representative)
                    # print('cluster_representatives: ', cluster_representatives)
                    # print('new cluster_representatives: ', new_cluster_representatives)
                    # idx = cluster_representatives.index(cluster_representative)
                    # cluster_representatives.remove(cluster_representative)
                    # cluster_representatives.insert(idx,new_cluster_representative)

        if round_change_flag:
            print("entering round change flag")
            # redo sequential assignment

            clusters = sequential_assignment(new_cluster_representatives, AS_similarity_data)

            cluster_representatives = deepcopy(new_cluster_representatives)

        else:
            break

        # start a new round
        print("round number: ", round_number)
        round_number += 1

    # return the clusters
    outputFileName = '../Data/similarity_clusters_test' + \
                     str(num_clusters) + '_' + similarity_index_name + '_' + date + '.json'

    file_out = open(outputFileName, 'w+')
    json.dump(clusters, file_out)
    file_out.close()
    # print(clusters)
    # print(outputFileName)

    return outputFileName


# helper methods for clustering_risk_accounted method
# switch to new_cluster_representative from old_cluster_representative
def switch_cluster_rep(new_cluster_rep, old_cluster_rep, clusters, AS_similarity_data):
    clusters_copy = deepcopy(clusters)
    old_relationships = clusters_copy.pop(old_cluster_rep)
    members = list(old_relationships.keys())
    clusters_copy[new_cluster_rep] = {}
    clusters_copy[new_cluster_rep].update({old_cluster_rep: AS_similarity_data[new_cluster_rep][old_cluster_rep]})
    for member in members:
        if member == new_cluster_rep:
            continue
        else:
            clusters_copy[new_cluster_rep].update({member: AS_similarity_data[new_cluster_rep][member]})

    return clusters_copy


# calculate the risk of a member AS being the representative AS
def calculate_increase_in_risk(member_AS, cluster_rep, usability_table, \
                               guards, \
                               guard_selection_probs):
    increase_in_risk = 0

    if member_AS == cluster_rep:
        return increase_in_risk
    else:
        suspect_flag = 1  # 0 if AS has at least one suspect_free guard, 1 otherwise
        for guard in guards:
            if usability_table[(member_AS, guard)] == False:
                increase_in_risk += guard_selection_probs[cluster_rep][guard]
            else:
                suspect_flag = 0
        increase_in_risk -= suspect_flag

        return increase_in_risk


def choose_least_risky_AS(old_cluster_rep, clusters, usability_table, \
                          all_ASes_list,
                          guard_selection_probs,\
                          guards):
    member_ASes = list(clusters[old_cluster_rep].keys())
    num_of_ASes = len(all_ASes_list)
    # guards = [g for (i, g), v in usability_table.items()]
    # num_guards = int(len(guards) / num_of_ASes)
    # print("num_guards = ", num_guards)
    # guards = guards[:num_guards]

    # first calculate min risk to be the risk of using the current cluster rep
    min_risk = 0
    least_risky_AS = old_cluster_rep
    for member_AS in member_ASes:
        min_risk += calculate_increase_in_risk(member_AS, old_cluster_rep, usability_table, \
                                               guards, \
                                               guard_selection_probs)

    print('min_risk is ', min_risk, ' old_cluster_rep is ', old_cluster_rep)
    # now, go through each member AS and see what the total risk of using them
    # as a cluster rep does to increase in risk of the cluster
    for member_AS in member_ASes:
        cur_risk = calculate_increase_in_risk(old_cluster_rep, member_AS, usability_table, \
                                              guards, \
                                              guard_selection_probs)
        for member_AS_inner in member_ASes:
            cur_risk += calculate_increase_in_risk(member_AS_inner, member_AS, usability_table, \
                                                   guards, \
                                                   guard_selection_probs)

        if cur_risk < min_risk:
            min_risk = cur_risk
            least_risky_AS = member_AS

    print('least_risky_AS is ', least_risky_AS, ' min_risk is ', min_risk)
    return least_risky_AS


# method assigning least risky AS as cluster rep
def clustering_risk_accounted(num_clusters, similarity_index_name, date, AS_similarity_file_name, \
                              guard_selection_probs_file_name):
    usability_table = np.load('../Data/usability_table.npy').item()

    # with open('../Data/guard_selection_probs.json') as f:
    with open(guard_selection_probs_file_name) as f:
        guard_selection_probs = json.load(f)

    # extract all the guards
    _, throwaway_probs = random.choice(list(guard_selection_probs.items()))
    guards = list(throaway_probs.keys())

    with open(AS_similarity_file_name) as data_file:
        AS_similarity_data = json.load(data_file)

    all_ASes_list = list(AS_similarity_data.keys())
    # generate the dictionary that shows the number of guards that each AS can usable
    # generated in generate_count_dict.py file
    # count_dict = generate_count_dict(usability_table, all_ASes_list)
    # with open('../Data/count_dict.json') as data_file:
    #     count_dict = json.load(data_file)

    # 1) choose a random AS
    first_AS_cluster_rep, first_AS_cluster_relationships = random.choice(list(AS_similarity_data.items()))

    # 2) choose k most dissimilar ASes to this AS to be cluster cluster_representatives
    cluster_representatives = choose_dissimilar_cluster_representatives(num_clusters, \
                                                                        first_AS_cluster_rep, \
                                                                        first_AS_cluster_relationships)

    # print(cluster_representatives)
    # 3) all other ASes are assigned to one of these cluster representatives. Assign member ASes
    # sequentially to the cluster representatives

    # 3a) Assign most similar AS to first cluster representative and so on
    clusters = sequential_assignment(cluster_representatives, AS_similarity_data)

    # 4) Within each cluster, if there's an AS that the member ASes are more similar to,
    # assign that as a cluster representative. Repeat for max_number_of_rounds
    max_number_of_rounds = 100
    round_number = 0

    # 4a) sum up the value of similarity in each cluster and divide by total number of
    #     ASes in the cluster to compare the similarity
    while round_number < max_number_of_rounds:

        # maintain a flag to keep track of any changes to the round
        round_change_flag = False

        # loop through each cluster representative
        if cluster_representatives:
            new_cluster_representatives = []
            new_cluster_representatives = deepcopy(cluster_representatives)
            for cluster_representative in cluster_representatives:

                if (len(clusters[cluster_representative]) != 0):
                    curr_avg_sim_val = sum(clusters[cluster_representative].values()) / \
                                       len(clusters[cluster_representative])
                else:
                    curr_avg_sim_val = 0

                member_ASes = list(clusters[cluster_representative].keys())
                change_flag = False;

                # compare avg_sim_val to curr_avg_sim_val to update
                for member_AS in member_ASes:
                    # start by adding the similarity val of the cluster representatives
                    # to the member AS under consideration, because it could be a member
                    # later
                    avg_sim_val = AS_similarity_data[cluster_representative][member_AS]
                    # loop through the other member ASes and add the similarity values
                    for member_AS_inner in member_ASes:
                        avg_sim_val += AS_similarity_data[member_AS][member_AS_inner]

                    # subtract the value self similarity value because we have double
                    # counted the member AS itself
                    avg_sim_val -= 1
                    avg_sim_val = avg_sim_val / (len(clusters[cluster_representative]))

                    # if avg_sim_val is > curr_avg_sim_val, remove the current cluster
                    # rep and make the member AS the cluster representative

                    if avg_sim_val > curr_avg_sim_val:
                        # print('old sim val: ', curr_avg_sim_val, ' new sim val: ', avg_sim_val)
                        # print("old cluster_representative: ", cluster_representative)
                        new_cluster_representative = member_AS
                        # print("new_cluster_representative: ", new_cluster_representative)
                        curr_avg_sim_val = avg_sim_val
                        change_flag = True
                        round_change_flag = True

                if change_flag:
                    # print("entering change flag")
                    new_cluster_representatives.remove(cluster_representative)
                    new_cluster_representatives.append(new_cluster_representative)
                    # print('cluster_representatives: ', cluster_representatives)
                    # print('new cluster_representatives: ', new_cluster_representatives)
                    # idx = cluster_representatives.index(cluster_representative)
                    # cluster_representatives.remove(cluster_representative)
                    # cluster_representatives.insert(idx,new_cluster_representative)

        if round_change_flag:
            # print("entering round change flag")
            # redo sequential assignment

            clusters = sequential_assignment(new_cluster_representatives, AS_similarity_data)

            cluster_representatives = deepcopy(new_cluster_representatives)

        else:
            break

        # start a new round
        # print("round number: ", round_number)
        round_number += 1

    # switch the cluster representatives to the least risky one
    for cluster_rep in list(clusters.keys()):
        new_cluster_rep = choose_least_risky_AS(cluster_rep, clusters, usability_table, \
                                                all_ASes_list, \
                                                guard_selection_probs,\
                                                guards)

        if new_cluster_rep != cluster_rep:
            clusters = switch_cluster_rep(new_cluster_rep, cluster_rep, clusters, \
                                          AS_similarity_data)

    # return the clusters
    outputFileName = '../Data/similarity_clusters_test' + \
                     str(num_clusters) + '_' + similarity_index_name + '_' + date + '.json'

    file_out = open(outputFileName, 'w+')
    json.dump(clusters, file_out)
    file_out.close()
    # print(clusters)
    # print(outputFileName)

    return outputFileName


# main method
def clustering(num_clusters, similarity_index_name, date, AS_similarity_file_name):
    with open(AS_similarity_file_name) as data_file:
        AS_similarity_data = json.load(data_file)

    # 1) choose a random AS
    first_AS_cluster_rep, first_AS_cluster_relationships = random.choice(list(AS_similarity_data.items()))

    # 2) choose k most dissimilar ASes to this AS to be cluster cluster_representatives
    cluster_representatives = choose_dissimilar_cluster_representatives(num_clusters, \
                                                                        first_AS_cluster_rep, \
                                                                        first_AS_cluster_relationships)

    # print(cluster_representatives)
    # 3) all other ASes are assigned to one of these cluster representatives. Assign member ASes
    # sequentially to the cluster representatives

    # 3a) Assign most similar AS to first cluster representative and so on
    clusters = sequential_assignment(cluster_representatives, AS_similarity_data)

    # 4) Within each cluster, if there's an AS that the member ASes are more similar to,
    # assign that as a cluster representative. Repeat for max_number_of_rounds
    max_number_of_rounds = 10000
    round_number = 0

    # 4a) sum up the value of similarity in each cluster and divide by total number of
    #     ASes in the cluster to compare the similarity
    while round_number < max_number_of_rounds:

        # maintain a flag to keep track of any changes to the round
        round_change_flag = False

        # loop through each cluster representative
        if cluster_representatives:
            new_cluster_representatives = []
            new_cluster_representatives = deepcopy(cluster_representatives)
            for cluster_representative in cluster_representatives:

                if (len(clusters[cluster_representative]) != 0):
                    curr_avg_sim_val = sum(clusters[cluster_representative].values()) / \
                                       len(clusters[cluster_representative])
                else:
                    curr_avg_sim_val = 0

                member_ASes = list(clusters[cluster_representative].keys())
                change_flag = False;

                # compare avg_sim_val to curr_avg_sim_val to update
                for member_AS in member_ASes:
                    # start by adding the similarity val of the cluster representatives
                    # to the member AS under consideration, because it could be a member
                    # later
                    avg_sim_val = AS_similarity_data[cluster_representative][member_AS]
                    # loop through the other member ASes and add the similarity values
                    for member_AS_inner in member_ASes:
                        avg_sim_val += AS_similarity_data[member_AS][member_AS_inner]

                    # subtract the value self similarity value because we have double
                    # counted the member AS itself
                    avg_sim_val -= 1
                    avg_sim_val = avg_sim_val / (len(clusters[cluster_representative]))

                    # if avg_sim_val is > curr_avg_sim_val, remove the current cluster
                    # rep and make the member AS the cluster representative

                    if avg_sim_val > curr_avg_sim_val:
                        # print('old sim val: ', curr_avg_sim_val, ' new sim val: ', avg_sim_val)
                        # print("old cluster_representative: ", cluster_representative)
                        new_cluster_representative = member_AS
                        # print("new_cluster_representative: ", new_cluster_representative)
                        curr_avg_sim_val = avg_sim_val
                        change_flag = True
                        round_change_flag = True

                if change_flag:
                    # print("entering change flag")
                    new_cluster_representatives.remove(cluster_representative)
                    new_cluster_representatives.append(new_cluster_representative)
                    # print('cluster_representatives: ', cluster_representatives)
                    # print('new cluster_representatives: ', new_cluster_representatives)
                    # idx = cluster_representatives.index(cluster_representative)
                    # cluster_representatives.remove(cluster_representative)
                    # cluster_representatives.insert(idx,new_cluster_representative)

        if round_change_flag:
            # print("entering round change flag")
            # redo sequential assignment

            clusters = sequential_assignment(new_cluster_representatives, AS_similarity_data)

            cluster_representatives = deepcopy(new_cluster_representatives)

        else:
            break

        # start a new round
        # print("round number: ", round_number)
        round_number += 1

    # return the clusters
    outputFileName = '../Data/similarity_clusters_test' + \
                     str(num_clusters) + '_' + similarity_index_name + '_' + date + '.json'

    file_out = open(outputFileName, 'w+')
    json.dump(clusters, file_out)
    file_out.close()
    # print(clusters)
    # print(outputFileName)

    return outputFileName


if __name__ == '__main__':
    clustering(10, 'jaccard', '200319', "../Data/ASSimilarityFile_jaccard_080319.json")

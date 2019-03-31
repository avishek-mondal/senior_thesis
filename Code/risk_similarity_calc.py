from collections import defaultdict
import functools
import sys
import json
import sys
import numpy as np

sys.path.append('../..')

from tempest import ip_to_asn
from  tempest.tor import relays
from tempest.tor import denasa
from tempest import pfi

def sokal_michener (outputChar='sokal_michener',\
                            nsf = "../Data/2016-10-01-00-00-00-network_state"):

    '''
    Load in all the data needed
    '''

    usability_table = np.load('../Data/usability_table.npy').item()

    guard_selection_probs = {}

    with open('../Data/guard_selection_probs.json') as f:
        guard_selection_probs = json.load(f)
    '''
    Initialize the similarity dictionary. Initially set all similarity values to 0.0
    '''
    output_similarity_dict = dict.fromkeys(list(guard_selection_probs.keys()),{})
    for i,v in output_similarity_dict.items():
        output_similarity_dict[i] = dict.fromkeys(list(guard_selection_probs.keys()),0.0)


    '''
    s(AS1, AS2): Sum over guards, for guard g_i with weight w_i (vanilla Tor weight aka consensus bandwidth),
    if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
    add w_i into total sum, and otherwise add 0

    '''

    '''
    First, get the vanilla Tor bandwidths
    '''
    network_state_vars = relays.fat_network_state(nsf)
    guard_fps = []
    for i, inner_dict in guard_selection_probs.items():
        for guard_fp, v in inner_dict.items():
            guard_fps.append(guard_fp)

    guard_weights = relays.pathsim_get_position_weights(guard_fps,
                                                        network_state_vars[0],
                                                        'g',
                                                        network_state_vars[4],
                                                        network_state_vars[5])
    total = sum(guard_weights.values())

    #normalize to get probabilities
    guard_weights = {k: v/total for k,v in guard_weights.items()}



    '''
    if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
    add w_i into total sum, and otherwise add 0
    '''
    for i, i_dict in output_similarity_dict.items():
        for j, v in i_dict.items():
            cp = 0
            ca = 0
            for guard in guard_weights.keys():
                if usability_table[(i,guard)] is True and usability_table[(j,guard)] is True:
                    cp+= guard_weights[guard]
                if usability_table[(i,guard)] is False and usability_table[(j,guard)] is False:
                    ca += guard_weights[guard]
            similarity = ca +cp
            i_dict[j] = similarity

    with open("../Data/ASSimilarityFile"+str(outputChar)+".json",'w') as file:
        json.dump(output_similarity_dict,file)



def jaccard (outputChar='jaccard',\
                            nsf = "../Data/2016-10-01-00-00-00-network_state"):

    '''
    Load in all the data needed
    '''

    usability_table = np.load('../Data/usability_table.npy').item()

    guard_selection_probs = {}

    with open('../Data/guard_selection_probs.json') as f:
        guard_selection_probs = json.load(f)
    '''
    Initialize the similarity dictionary. Initially set all similarity values to 0.0
    '''
    output_similarity_dict = dict.fromkeys(list(guard_selection_probs.keys()),{})
    for i,v in output_similarity_dict.items():
        output_similarity_dict[i] = dict.fromkeys(list(guard_selection_probs.keys()),0.0)


    '''
    s(AS1, AS2): Sum over guards, for guard g_i with weight w_i (vanilla Tor weight aka consensus bandwidth),
    if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
    add w_i into total sum, and otherwise add 0

    '''

    '''
    First, get the vanilla Tor bandwidths
    '''
    network_state_vars = relays.fat_network_state(nsf)
    guard_fps = []
    for i, inner_dict in guard_selection_probs.items():
        for guard_fp, v in inner_dict.items():
            guard_fps.append(guard_fp)

    guard_weights = relays.pathsim_get_position_weights(guard_fps,
                                                        network_state_vars[0],
                                                        'g',
                                                        network_state_vars[4],
                                                        network_state_vars[5])
    total = sum(guard_weights.values())

    #normalize to get probabilities
    guard_weights = {k: v/total for k,v in guard_weights.items()}



    '''
    if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
    add w_i into total sum, and otherwise add 0
    '''
    for i, i_dict in output_similarity_dict.items():
        for j, v in i_dict.items():
            similarity = 0
            numerator = 0
            denominator = 0
            for guard in guard_weights.keys():
                if usability_table[(i,guard)] is True and usability_table[(j,guard)] is True:
                    numerator+= guard_weights[guard]
                if usability_table[(i,guard)] is True or usability_table[(j,guard)] is True:
                    denominator += guard_weights[guard]
            similarity = numerator/denominator if denominator != 0 else 1
            i_dict[j] = similarity

    with open("../Data/ASSimilarityFile"+str(outputChar)+".json",'w') as file:
        json.dump(output_similarity_dict,file)




def calculate_risk_similarity (outputChar='risk_similarity_metric',\
                            nsf = "../Data/2016-10-01-00-00-00-network_state"):

    '''
    Load in all the data needed
    '''

    usability_table = np.load('../Data/usability_table.npy').item()

    guard_selection_probs = {}

    with open('../Data/guard_selection_probs.json') as f:
        guard_selection_probs = json.load(f)
    '''
    Initialize the similarity dictionary. Initially set all similarity values to 0.0
    '''
    output_similarity_dict = dict.fromkeys(list(guard_selection_probs.keys()),{})
    for i,v in output_similarity_dict.items():
        output_similarity_dict[i] = dict.fromkeys(list(guard_selection_probs.keys()),0.0)


    '''
    s(AS1, AS2): Sum over guards, for guard g_i with weight w_i (vanilla Tor weight aka consensus bandwidth),
    if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
    add w_i into total sum, and otherwise add 0

    '''

    '''
    First, get the vanilla Tor bandwidths
    '''
    network_state_vars = relays.fat_network_state(nsf)
    guard_fps = []
    for i, inner_dict in guard_selection_probs.items():
        for guard_fp, v in inner_dict.items():
            guard_fps.append(guard_fp)

    guard_weights = relays.pathsim_get_position_weights(guard_fps,
                                                        network_state_vars[0],
                                                        'g',
                                                        network_state_vars[4],
                                                        network_state_vars[5])
    total = sum(guard_weights.values())

    #normalize to get probabilities
    guard_weights = {k: v/total for k,v in guard_weights.items()}



    '''
    if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
    add w_i into total sum, and otherwise add 0
    '''
    for i, i_dict in output_similarity_dict.items():
        for j, v in i_dict.items():
            similarity = 0
            for guard in guard_weights.keys():
                if usability_table[(i,guard)] is True and usability_table[(j,guard)] is True:
                    similarity+= guard_weights[guard]
            i_dict[j] = similarity

    with open("../Data/ASSimilarityFile"+str(outputChar)+".json",'w') as file:
        json.dump(output_similarity_dict,file)

#
#
# def calculate_risk_similarity(outputChar='RiskMetric',\
#                             nsf = "../Data/2016-10-01-00-00-00-network_state"):
#     '''
#     Load in all the data needed
#     '''
#
#     usability_table = np.load('../Data/usability_table.npy').item()
#
#     '''
#     Initialize the similarity dictionary. Initially set all similarity values to 0.0
#     '''
#     output_similarity_dict = dict.fromkeys(list(guard_selection_probs.keys()),{})
#     for i,v in output_similarity_dict.items():
#         output_similarity_dict[i] = dict.fromkeys(list(guard_selection_probs.keys()),0.0)
#
#
#     '''
#     s(AS1, AS2): Sum over guards, for guard g_i with weight w_i (vanilla Tor weight aka consensus bandwidth),
#     if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
#     add w_i into total sum, and otherwise add 0
#
#     '''
#
#     '''
#     First, get the vanilla Tor bandwidths
#     '''
#     network_state_vars = relays.fat_network_state(nsf)
#     guard_fps = []
#     for i, inner_dict in guard_selection_probs.items():
#         for guard_fp, v in inner_dict.items():
#             guard_fps.append(guard_fp)
#
#     guard_weights = relays.pathsim_get_position_weights(guard_fps,
#                                                         network_state_vars[0],
#                                                         'g',
#                                                         network_state_vars[4],
#                                                         network_state_vars[5])
#     total = sum(guard_weights.values())
#
#     #normalize to get probabilities
#     guard_weights = {k: v/total for k,v in guard_weights.items()}
#
#
#
#     '''
#     if AS1 and AS2 agree on usability of g_i (i.e. if g_i is usable for both or unusable for both) then
#     add w_i into total sum, and otherwise add 0
#     '''
#     for i, i_dict in output_similarity_dict.items():
#         for j, v in i_dict.items():
#             similarity = 0
#             for guard in guard_weights.keys():
#                 if usability_table[(i,guard)] == usability_table[(j,guard)]:
#                     similarity+= guard_weights[guard]
#             i_dict[j] = similarity
#
#     with open("../Data/ASSimilarityFile"+str(outputChar)+"risk_similarity.json",'w') as file:
#         json.dump(output_similarity_dict,file)
#
#


def calculate_self_risk_similarity(guard_selection_filename = '../Data/guard_selection_probs.json',outputChar='RiskMetric'):
    '''
    Load in all the data needed
    '''
    with open(guard_selection_filename) as f:
        guard_selection_probs = json.load(f)

    usability_table = np.load('../Data/usability_table.npy').item()

    '''
    Initialize the similarity dictionary. Initially set all similarity values to 0.0
    '''
    output_similarity_dict = dict.fromkeys(list(guard_selection_probs.keys()),{})
    for i,v in output_similarity_dict.items():
        output_similarity_dict[i] = dict.fromkeys(list(guard_selection_probs.keys()),0.0)


    '''
    Now, do the following steps -
    1) extract all guardfps with non-zero values for the representative ASes

    2)For each member AS, look at the usability table for the particular guard fp.
    If FALSE, sum up the probability, and call the metric risk

    3)Plot this risk against how similar the member AS is to the representative AS.

    '''

    for rep_AS, inner_similarity_dict in output_similarity_dict.items():
        curr_guard_dict = guard_selection_probs[rep_AS]

        for member_AS, similarity_val in inner_similarity_dict.items():
            using_alias_risk = 0
            self_risk = 1
            for guard_fps, probability in curr_guard_dict.items():
                if probability != 0 and usability_table[(member_AS, guard_fps)] == False:
                    using_alias_risk = using_alias_risk + probability

                if usability_table[(member_AS, guard_fps)] == True:
                    #if there is at least one suspect free AS, self-risk is 0
                    self_risk = 0


            inner_similarity_dict[member_AS] = 1 - (using_alias_risk - self_risk)

    with open("../Data/ASSimilarityFile"+str(outputChar)+"26122018.json",'w') as file:
        json.dump(output_similarity_dict,file)




if __name__ == '__main__':
    #generate_usability_table()
    calculate_increase_risk()

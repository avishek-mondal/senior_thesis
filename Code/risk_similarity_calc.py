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

def calculate_risk_similarity(guard_slection_filename = '../Data/guard_selection_probs.json',outputChar='RiskMetric'):
    '''
    Load in all the data needed
    '''
    with open(guard_slection_filename) as f:
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
            risk = 0
            for guard_fps, probability in curr_guard_dict.items():
                if probability != 0 and usability_table[(member_AS, guard_fps)] == False:
                    print(rep_AS, member_AS, guard_fps, probability, risk)
                    risk = risk + probability
            inner_similarity_dict[member_AS] = 1 - risk

    with open("../Data/ASSimilarityFile"+str(outputChar)+"1.json",'w') as file:
        file.write(json.dumps(output_similarity_dict))







if __name__ == '__main__':
    #generate_usability_table()
    calculate_risk_similarity()

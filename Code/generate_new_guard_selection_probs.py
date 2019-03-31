import json
import numpy as np

def generate_new_guard_selection_probs():

    with open('../Data/guard_selection_probs.json') as f:
        guard_selection_probs = json.load(f)

    with open('../Data/guard_weights.json') as f:
        guard_weights = json.load(f)

    ASes = list(guard_selection_probs.keys())
    guards = list(guard_weights.keys())
    guard_selection_probs_new_261218 = {}

    for AS in ASes:
        guard_selection_probs_new_261218[AS] = {}
        for guard in guards:
            guard_selection_probs_new_261218[AS][guard] = 0
            if usability_table[(AS, guard)] == True:
                guard_selection_probs_new_261218[AS][guard] = guard_weights[guard]
                print(AS, guard, guard_weights[guard])

        total = sum(guard_selection_probs_new_261218[AS].values())
        if total !=0:
            guard_selection_probs_new_261218[AS] = {k: v/total for k,v in guard_selection_probs_new_261218[AS].items()}


    with open('../Data/guard_selection_probs_new_261218.json', 'w') as f:
        json.dump(guard_selection_probs_new_261218, f)

if __name__ = '__main__':
    generate_new_guard_selection_probs()
    

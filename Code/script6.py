import json
import numpy as np

with open('../Data/guard_selection_probs.json') as f:
    guard_selection_probs = json.load(f)

with open('../Data/guard_weights.json') as f:
    guard_weights = json.load(f)

usability_table = np.load('../Data/usability_table.npy').item()

ASes = list(guard_selection_probs.keys())
guards = list(guard_weights.keys())
count = 0

guard_selection_probs_new_261218 = {}
with open('../Data/guard_selection_probs_new_261218.json') as f:
    guard_selection_probs_new_261218 = json.load(f)

for AS in ASes:
    for guard in guards:
        if usability_table[(AS, guard)] == False and guard_selection_probs[AS][guard]!= 0:
            print("This is an error! AS is ", AS, ' and guard is ', guard, ' probability is ', guard_selection_probs[AS][guard])
            count+=1
print(count)

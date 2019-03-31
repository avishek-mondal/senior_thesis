import json
import math
from copy import deepcopy
import random
import sys
import matplotlib.pyplot as plt
import numpy as np


with open('../Data/guard_selection_probs.json') as f:
    guard_selection_probs = json.load(f)


with open('../Data/guard_weights.json') as f:
    guard_weights = json.load(f)

usability_table = np.load('../Data/usability_table.npy').item()

# ASes = list(guard_selection_probs.keys())
# another way of getting ASes
with open('../Data/Top95ASes.txt','r') as f:
    ASes = [line.rstrip() for line in f]

guards = list(guard_weights.keys())

y = []

for AS in ASes:
    d = {(i,j): v for (i,j), v in usability_table.items() if v == True and i == AS}
    y.append(len(d))

f = plt.figure()
plt.plot(ASes, y,'ro')
plt.title("Number of usable guards")
plt.xlabel("ASes")
plt.ylabel("Number of guards")
output_filename = "../Plots/plot_usable_guards_vs_AS.png"
f.savefig(output_filename, bbox_inches = "tight")

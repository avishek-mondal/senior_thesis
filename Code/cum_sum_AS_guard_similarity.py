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

# y = sorted(y)
y1 = np.cumsum(sorted(y))
y1 = y1/max(y1)

y2 = sorted(y)

print(y1[int(len(ASes)/2)])
print(y2[int(len(ASes)/2)])

f = plt.figure()
plt.plot([i for i in range(len(ASes))], y1,'r')
plt.title("Cumulative distribution of usable guards")
plt.xlabel("Number of ASes")
plt.ylabel("Percentage of guards")
output_filename = "../Plots/plot_usable_guards_vs_AS_cumulative_percentage.png"
f.savefig(output_filename, bbox_inches = "tight")

f = plt.figure()
plt.plot([i for i in range(len(ASes))], y2,'r')
plt.title("Cumulative distribution of usable guards")
plt.xlabel("Number of ASes")
plt.ylabel("Percentage of guards")
output_filename = "../Plots/plot_usable_guards_vs_AS_cumulative_sorted.png"
f.savefig(output_filename, bbox_inches = "tight")

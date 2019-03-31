import json
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import norm


inp_dict = {}
with open('../Data/similarity_clusters_10_080119.json') as f:
    inp_dict = json.load(f)

rep_ASes = list(inp_dict.keys())

#extract values to plot
values = []
for AS in rep_ASes:
    values.append(list(inp_dict[AS].values()))

sorted_values = sorted(values[0])
cum_sum = np.cumsum(sorted_values)
cum_sum = cum_sum/max(cum_sum)

f = plt.figure()
plt.plot(sorted_values,cum_sum)
plt.show()
f.savefig("../Plots/CDFplot_09012019.png", bbox_inches='tight')

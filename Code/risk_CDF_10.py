import json
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import norm


inp_dict = {}
with open('../Data/ASSimilarityFileRiskMetricincrease_risk.json') as f:
    inp_dict = json.load(f)

rep_ASes = list(inp_dict.keys())

#extract values to plot
values = []
for AS in rep_ASes:
    values.append(list(inp_dict[AS].values()))

f = plt.figure()

for i,value in enumerate(values):
    sorted_values = sorted(value)
    cum_sum = np.cumsum(sorted_values)
    cum_sum = cum_sum/max(cum_sum)
    legend_title = "Cluster " + str(i+1)
    plt.plot(sorted_values,cum_sum, label = legend_title)

# plt.legend(loc='upper left')
plt.xlabel('Risk')
plt.ylabel('Cumulative Distribution')
plt.title('Cumulative distribution of risk within each cluster')
plt.show()
f.savefig("../Plots/risk_CDF_plot_09012019.png", bbox_inches='tight')

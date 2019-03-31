import numpy as np
import json
import matplotlib.pyplot as plt


'''
Load all the data we need - usability table, the representative ASes, and the
json file with the guardfps probabilities
'''
#usability table
usability_table = np.load('../Data/usability_table.npy').item()

#get the representative rep_ASes
similarity_clusters = {}
with open('../Data/similarity_clusters_10_05112018.json') as f:
    similarity_clusters = json.load(f)


#get the guardfps probabilites
guard_selection_probs = {}
with open('../Data/guard_selection_probs.json') as f:
    guard_selection_probs = json.load(f)

list_of_guards = []
for i, v in guard_selection_probs['6128'].items():
    list_of_guards.append(i)

'''
Now, do the following steps -
1) extract all guardfps with non-zero values for the representative ASes

2)For each member AS, look at the usability table for the particular guard fp.
If FALSE, sum up the probability, and call the metric risk

3) If there an AS has no suspect free guards, we subtract 1 from the 'risk' calculation, because
   we are looking at increase in risk

3)Plot this risk against how similar the member AS is to the representative AS.

'''


x = []  #x - axis to show similarity
y = []  #y-axis to show risk
count = 0


for rep_AS, similarity_dict in similarity_clusters.items():
    for member_AS, similarity_val in similarity_dict.items():
        risk = 0
        for guardfps in list_of_guards:
            if usability_table[(member_AS,guardfps)] == False:
                risk += guard_selection_probs[rep_AS][guardfps]




        count +=   1
        x.append(similarity_val)
        y.append(risk)


'''
(3) Now plot the cumulative distribution of the increase in risk values of all
ASes
'''
print(len(x), len(y), count)
f = plt.figure()
sorted_values = sorted(y)
cum_sum = np.cumsum(sorted_values)
cum_sum = cum_sum = cum_sum/max(cum_sum)
plt.plot(sorted_values,cum_sum)
# bottom, top = plt.xlim()
# plt.xlim(0.8,top)

plt.xlabel('Increase in Risk')
plt.ylabel('CDF')
plt.title(\
'Plot showing CDF of increase in risk (baseline metric)')

plt.show()
f.savefig("../Plots/risk_global_CDF_plot_05112018.png", bbox_inches='tight')

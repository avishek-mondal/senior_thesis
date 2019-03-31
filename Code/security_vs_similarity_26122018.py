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
with open('../Data/similarity_clusters_10_261218.json') as f:
    similarity_clusters = json.load(f)


#get the guardfps probabilites
guard_selection_probs = {}
with open('../Data/guard_selection_probs_new_261218.json') as f:
    guard_selection_probs = json.load(f)

'''
Now, do the following steps -
1) extract all guardfps with non-zero values for the representative ASes

2)For each member AS, look at the usability table for the particular guard fp.
If FALSE, sum up the probability, and call the metric risk

3)Plot this risk against how similar the member AS is to the representative AS.

'''
x = []  #x - axis to show similarity
y = []  #y-axis to show risk
count = 0
for rep_AS, similarity_dict in similarity_clusters.items():
    curr_guard_dict = guard_selection_probs[rep_AS]
    '''
    (1) Extract all guardfps with non 0 value for rep ASes
    '''
    possible_guard_choice = {}
    for guard_fps, probability in curr_guard_dict.items():
        if probability != 0:
            possible_guard_choice[guard_fps] = probability

    '''
    2)For each member AS, look at the usability table for the particular guard fp.
    If FALSE, sum up the probability, and call the metric risk
    '''
    for member_AS, similarity in similarity_dict.items():
        risk = 0
        for guard_fps, probability in possible_guard_choice.items():
            if usability_table[(member_AS, guard_fps)] == False:
                risk = risk + probability
        count+=1
        x.append(similarity)
        y.append(risk)
        if similarity == 0 and risk==0:
            print('rep_AS :', rep_AS, ' member_AS: ', member_AS)


'''
(3) Now plot
'''
print(len(x), len(y), count)
f = plt.figure()
plt.plot(x,y,'ro')
# bottom, top = plt.xlim()
# plt.xlim(0.8,top)

plt.xlabel('Similarity')
plt.ylabel('Risk')
plt.title(\
'Plot showing relationship between risk of choosing \n \
a guard that will have a suspect AS against similarity \n \
of member AS to cluster representative')

plt.show()
f.savefig("../Plots/security_vs_similarity_26122018.png", bbox_inches='tight')

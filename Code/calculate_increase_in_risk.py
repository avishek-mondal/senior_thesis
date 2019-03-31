import numpy as np
import json
import matplotlib.pyplot as plt




def security_calc (similarityClusterFileName, num_clusters, similarity_index_name, date):
    '''
    Load all the data we need - usability table, the representative ASes, and the
    json file with the guardfps probabilities
    '''
    #usability table

    usability_table = np.load('../Data/usability_table.npy').item()

    #get the representative rep_ASes
    similarity_clusters = {}
    with open(similarityClusterFileName) as f:
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
            suspect_flag = 1 #0 if AS has at least one suspect_free guard, 1 otherwise
            for guardfps in list_of_guards:
                if usability_table[(member_AS,guardfps)] == False:
                    risk += guard_selection_probs[rep_AS][guardfps]
                else:
                    suspect_flag = 0

            risk -= suspect_flag

            count +=   1
            if similarity_val > 0.95 and risk > 0.95:
                print('rep_AS is '+ rep_AS+ ' member_AS is '+member_AS+ ' increase in risk is '+ str(risk) + ' similarity_val is '+str(similarity_val))
            x.append(similarity_val)
            y.append(risk)


    '''
    (3) Now plot
    '''
    print(len(x), len(y), count)
    plot_risk_similarity(x,y,num_clusters,similarity_index_name, date)

def plot_risk_similarity(x,y, num_clusters, similarity_index_name, date):

    f = plt.figure()
    plt.plot(x,y,'ro')
    # bottom, top = plt.xlim()
    # plt.xlim(0.8,top)

    plt.xlabel('Similarity')
    plt.ylabel('Increase in Risk')
    plt.title(\
    'Plot showing relationship between risk of choosing \n \
    a guard that will have a suspect AS against similarity \n \
    of member AS to cluster representative')

    output_filename = '../Plots/security_vs_similarity_'+ num_clusters+ '_'+ similarity_index_name+'_'+date+'.png'
    f.savefig(output_filename, bbox_inches='tight')
    plot_cdf(y,num_clusters, similarity_index_name, date)


def plot_cdf(y,num_clusters, similarity_index_name, date):
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
    'Plot showing CDF of increase in risk (' + similarity_index_name + ' '+ date + ')')

    f.savefig("../Plots/risk_global_CDF_plot_" + num_clusters+ '_'+ similarity_index_name+'_'+date+'.png', bbox_inches='tight')

# if __name__ == '__main__':
# 	security_calc()

import json
import matplotlib.pyplot as plt
import numpy as np
import pylab


def whisker_plot(filename):

    inp_dict = {}
    with open('../Data/'+filename) as f:
        inp_dict = json.load(f)

    rep_ASes = list(inp_dict.keys())

    #extract values to plot
    values = []
    for AS in rep_ASes:
        values.append(list(inp_dict[AS].values()))

    #plot!
    f = plt.figure()
    plt.boxplot(values)
    plt.xlabel("Cluster number")
    plt.ylabel("Similarity")
    plt.title("Whisker plot showing similarity statistics of ASes in each cluster for 10 clusters")
    plt.show()
    f.savefig("../Plots/whisker_plot_risk_similarity_10_210319.png", bbox_inches='tight')

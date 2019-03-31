import json
import math
from copy import deepcopy
import random
import sys
import matplotlib
import matplotlib.pyplot as plt
import operator

def visualize(AS_similarity_file_name):
    with open(AS_similarity_file_name) as data_file:
        AS_similarity_data = json.load(data_file)

    AS_to_visualize = '10316'
    # sort by values
    lists = sorted(AS_similarity_data['6128'].items(), key = operator.itemgetter(1))

    x,y = zip(*lists)

    f = plt.figure()
    matplotlib.rcParams.update({'font.size':5})


    plt.plot(x,y,'ro')
    plt.title("Similarity distribution of AS "+AS_to_visualize)
    plt.xlabel("ASes")


    plt.ylabel("Similarity Values")



    output_filename = "../Plots/visualize_"+AS_to_visualize+".png"
    f.savefig(output_filename, bbox_inches = "tight")

if __name__ == '__main__':
    visualize('../Data/ASSimilarityFile_jaccard_new_050219.json')

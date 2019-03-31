import json
import numpy as np

def generate_count_dict(usability_table,all_ASes_list):
    count_dict = {}
    for AS in all_ASes_list:
        d = {(i,j): v for (i,j), v in usability_table.items() if v == True and i == AS}
        count_dict[AS] = len(d)
    return count_dict


usability_table = np.load('../Data/usability_table.npy').item()

AS_similarity_file_name = "../Data/ASSimilarityFile_jaccard_210319.json"
with open(AS_similarity_file_name) as data_file:
    AS_similarity_data = json.load(data_file)

all_ASes_list = list(AS_similarity_data.keys())
count_dict = generate_count_dict(usability_table, all_ASes_list)

file_out = open('../Data/count_dict.json', 'w+')
json.dump(count_dict, file_out)
file_out.close()

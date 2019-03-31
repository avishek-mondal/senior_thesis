for i, i_dict in output_similarity_dict.items():
    for j, v in i_dict.items():
        similarity = 0
        for guard in guard_weights.keys():
            if usability_table[(i,guard)] == usability_table[(j,guard)]:
                similarity+= guard_weights[guard]
        i_dict[j] = similarity

outputChar='RiskMetric'
with open("../Data/ASSimilarityFile"+str(outputChar)+"risk_similarity.json",'w') as file:
    json.dump(output_similarity_dict,file)

import sys
import json
import ASWeightComparisonDeNasa

sys.path.append('../../tempest')

from tempest.tor import denasa
from tempest import ip_to_asn
from tempest import pfi

#get 95 Top ASes
inp_array = []
with open('../Data/Top95ASes.txt','r') as file:
    for i in file.readlines():
        inp_array.append(i.rstrip("\n"))


nsf = "../Data/2016-10-01-00-00-00-network_state"
pft = ip_to_asn.prefix_tree_from_pfx2as_file("../Data/routeviews-rv2-20161001-1200.pfx2as")
my_pfi = pfi.PFI("../Data/libspookyhash.so", "../Data/20180601_paths.txt", "../Data/20180601_index.bin")
my_pfi.load()

# denasa_output_json = json.dumps(denasa.compute_denasa_guard_selection_probs(["6128","25019","8972","6893","15467"], nsf, pft, my_pfi))
denasa_output_json = json.dumps(denasa.compute_denasa_guard_selection_probs(inp_array, nsf, pft, my_pfi))

with open("../Data/guard_selection_probs.json", "w") as file:
    file.write(denasa_output_json)

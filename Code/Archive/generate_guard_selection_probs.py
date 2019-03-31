import sys
import json
import numpy as np
# import ASWeightComparisonDeNasa

sys.path.append('../../tempest')

from tempest.tor import denasa
from tempest import ip_to_asn
from tempest import pfi
from tempest.tor import relays




#get 95 Top ASes
inp_array = []
with open('../Data/Top95ASes.txt','r') as file:
    for i in file.readlines():
        inp_array.append(i.rstrip("\n"))


nsf = "../Data/2016-10-01-00-00-00-network_state"
pft = ip_to_asn.prefix_tree_from_pfx2as_file("../Data/routeviews-rv2-20161001-1200.pfx2as")
my_pfi = pfi.PFI("../Data/libspookyhash.so", "../Data/20180601_paths.txt", "../Data/20180601_index.bin")
my_pfi.load()

network_state_vars = relays.fat_network_state(nsf)

guard_fp_to_ip = relays.get_guards(network_state_vars[0],
                                   network_state_vars[1])

guard_fp_to_asns =\
        relays.make_relay_fp_to_asns_dict(guard_fp_to_ip, pft)

guard_fps = []
for guard_fp, asns in guard_fp_to_asns.items():
    if asns is not None:
        guard_fps.append(guard_fp)

guard_selection_probs = denasa.compute_denasa_guard_selection_probs(inp_array, nsf, pft, my_pfi)


denasa_output_json = json.dumps(guard_selection_probs)
with open("../Data/guard_selection_probs.json", "w") as file:
    file.write(denasa_output_json)


usability_table = denasa.make_client_guard_usability_table(inp_array,guard_fps, guard_fp_to_asns, my_pfi)
np.save('../Data/usability_table.npy', usability_table)

from collections import defaultdict
import functools
import sys
import json
import sys
import numpy as np

sys.path.append('../..')

from tempest import ip_to_asn
from  tempest.tor import relays
from tempest.tor import denasa
from tempest import pfi


nsf = "../Data/2016-10-01-00-00-00-network_state"
pft = ip_to_asn.prefix_tree_from_pfx2as_file("../Data/routeviews-rv2-20161001-1200.pfx2as")
my_pfi = pfi.PFI("../Data/libspookyhash.so", "../Data/20180601_paths.txt", "../Data/20180601_index.bin")
my_pfi.load()

#load in json file
with open('../Data/guard_selection_probs.json') as f:
    inp_dict = json.load(f)

top_ASes = list(inp_dict.keys())
guard_fps = list(inp_dict['6128'].keys())

network_state_vars = relays.fat_network_state(nsf)

guard_fp_to_ip = relays.get_guards(network_state_vars[0],
                                     network_state_vars[1])
guard_fp_to_asns =\
          relays.make_relay_fp_to_asns_dict(guard_fp_to_ip, pft)

usability_table = denasa.make_client_guard_usability_table(top_ASes,guard_fps, guard_fp_to_ip, my_pfi)


np.save('../Data/usability_table.npy', usability_table)

#Call this using python check_security.py | less

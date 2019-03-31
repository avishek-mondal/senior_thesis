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


def generate_usability_table(guard_slection_filename = '../Data/guard_selection_probs.json', \
                             nsf = "../Data/2016-10-01-00-00-00-network_state",\
                             pfx2as = "../Data/routeviews-rv2-20161001-1200.pfx2as",\
                             libspookyhash_file = "../Data/libspookyhash.so",\
                             paths_text_file = "../Data/20180601_paths.txt", \
                             index_bin_file = "../Data/20180601_index.bin"):



    pft = ip_to_asn.prefix_tree_from_pfx2as_file(pfx2as)
    my_pfi = pfi.PFI(libspookyhash_file,paths_text_file,index_bin_file)
    my_pfi.load()

    #load in json file
    with open(guard_slection_filename) as f:
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

if __name__ == '__main__':
    generate_usability_table()

import networkx as nx

from toolbox import *

if __name__ == "__main__":
    bpd = 144 # number of blocks per day on average
    # blockhash = get_latest_block_hash()
    first_block = get_block_from_height(729655+bpd*1)
    download_n_blocks(first_block, bpd)
    # G = nx.read_adjlist("./data/block_729448_144.adjlist", create_using=nx.DiGraph)
    # # G = nx.read_adjlist("./data/block_729655_144.adjlist", create_using=nx.DiGraph)
    # print_all_metrics(G)

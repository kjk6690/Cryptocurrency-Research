import networkx as nx

from toolbox import *

if __name__ == "__main__":
    bpd = 144 # number of blocks per day on average
    blockhash = get_latest_block_hash()
    download_n_blocks('00000000000000000001109f4bf0bcbecea18136ffe0a8ffb437c2c0b6ac433f', bpd)
    G = nx.read_adjlist("./data/block_729448_144.adjlist", create_using=nx.DiGraph)
    G = nx.read_adjlist("./data/block_729655_144.adjlist", create_using=nx.DiGraph)
    print_all_metrics(G)

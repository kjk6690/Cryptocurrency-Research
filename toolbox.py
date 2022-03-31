import requests # Gets website JSON information
import networkx as nx # Used for graphs
import json # Used to write to JSON file
import numpy as np # Used for adding arrays together
from varname import nameof
import os
import matplotlib.pyplot as plt
import statistics as stats
import pandas as pd

url = "https://blockchain.info/"

def get_latest_block_hash():
    """
    Get hash number of the latest block on blockchain
    :return: hash number
    """
    response = requests.get(url + "latestblock")
    if response.status_code == 200: # If request is successful
        return response.json()['hash'] # Return blockhash

def get_block(blockhash):
    """
    Get block old_data given a blockhash
    :param blockhash: the hash for the block to get old_data of
    :return: dictionary containing block info (including transaction list)
    """
    response = requests.get(url + "rawblock/" + blockhash)
    if response.status_code == 200:  # If request is successful, continue
        return response.json() # Return block

def get_tx(tx_hash):
    """
    Get transaction old_data
    :param tx_hash: hash for this specific transaction
    :return: dictionary of transaction old_data
    """
    response = requests.get(url + "rawtx/" + tx_hash)
    if response.status_code == 200:  # If request is successful, continue
        return response.json() # Return tx

def get_nth_prev_block(blockhash, n):
    """
    Gets nth previous block on the block from a given hash
    :param blockhash: starting blockhash
    :param n: number of blocks down
    :return: block data for the nth previous block
    """
    block = get_block(blockhash)
    for i in range(0,n):
        block = get_block(block['prev_block'])
    return block

def create_transaction_CBG(tx_details):
    """
    Creates transaction complete Bipartite Graph
    :param tx_details: transaction old_data
    :return: networkX Complete bipartite graph
    """
    input_addr = []  # empty  input address sets
    output_addr = []  # empty output address sets
    inputs = tx_details['inputs']  # Get input  old_data
    outputs = tx_details['out']  # Get output old_data
    for idx in range(len(inputs)):  # Loop over inputs
        # If address present, add to input_addr set
        try: input_addr.append(inputs[idx]['prev_out']['addr'])
        # If address not present, add supernode to represent mining reward
        except: input_addr.append(-1)
    # Add output addresses to output_addr. When several BTC chunks are given to the same address,
    # the 'addr' property is not present, so we skip that address
    [output_addr.append(outputs[idx]['addr']) for idx in range(len(outputs)) \
     if ('addr' in outputs[idx].keys() and outputs[idx]['addr'] not in input_addr)]
    # Make directed graph for transaction
    CBG = nx.DiGraph()
    CBG.add_nodes_from(input_addr)
    CBG.add_nodes_from(output_addr)
    CBG.add_edges_from(np.transpose([np.tile(input_addr, len(output_addr)), np.repeat(output_addr, len(input_addr))]))
    return CBG

def create_block_graph(block, progress_updates=True):
    """
    Create networkX graph from block old_data
    :param block: block old_data containing transactions
    :param progress_updates: if True, prints progress updates
    :return: transaction graph for the given block
    """
    G = nx.DiGraph()
    txs = block['tx']

    num_tx = len(txs)
    counter = 1

    for tx in txs:
        if progress_updates:
            print("{:3.2f}%".format(counter*100/num_tx))
            try:
                tx_details = get_tx(tx['hash'])
                CBG = create_transaction_CBG(tx_details)
                G.add_nodes_from(CBG)
                G.add_edges_from(CBG.edges())
            except:
                print("Error @ tx {:s}, block {:s} ".format(tx['hash'], block['hash']))
            counter += 1
    return G


def download_n_blocks(first_block_hash, n, progress_updates=True):
    """
    Creates a file with transaction graphs of the last n blocks on the blockchain
    This saves to a file after every block to prevent data loss from errors
    File format: "block_{height}_{i}"
    where height is the height of the first block on the blockchain
    and i is the iteration that this function has saved thus far
    :param first_block_hash: the block hash of the highest block to pull from
    :param n: number of blocks to pull from
    :param progress_updates: if True, prints progress updates
    """
    G = nx.DiGraph()

    block_hash = first_block_hash
    block = get_block(block_hash)
    height = str(block['height'])

    print("first block hash:", block_hash)
    nx.write_adjlist(G,"./data/block_"+height+"_0.adjlist")
    for i in range(0,n):
        if progress_updates:
            print("{:d} blocks processed out of {:d} ".format(i,n))
            print("block hash {:s}".format(block_hash))
        try:
            subgraph = create_block_graph(block, progress_updates=progress_updates)
            G = nx.read_adjlist("./data/block_"+height+"_"+str(i)+".adjlist")
            G.add_nodes_from(subgraph)
            G.add_edges_from(subgraph.edges())
            nx.write_adjlist(G, "./data/block_"+height+"_"+str(i+1)+".adjlist")
            del G; os.remove("./data/block_"+height+"_"+str(i)+".adjlist")
            block_hash = block['prev_block']
            if i < n: block = get_block(block_hash)
        except: print("Error @ block {:s} tx ".format(block_hash))
    if progress_updates:
        print(" {:d} blocks processed out of {:d} ".format(n, n))


def draw_graph_from_file(filename,circular=False,with_labels=False, create_using=nx.Graph):
    """
    Given an adjacency list representation of a graph, draw the graph
    Note: May take a long time if Graph is large
    :param filename: filename of adjacency list
    :param circular: Plot in circular format. Will draw graph faster
    :param with_labels: If true, plots with labels
    :param create_using: The adjacency list will be processed to make a graph of the specified type (e.g. nx.DiGraph for directed graph)
    """
    plt.figure()
    G = nx.read_adjlist(filename, create_using=create_using)
    print("Made Graph")
    if circular:
        nx.draw_circular(G, with_labels=with_labels, node_size=2, linewidths=1)
    else:
        nx.draw_networkx(G, with_labels=with_labels, node_size=2, linewidths=1)
    print("Drawn")
    plt.show()
    return G

######### METRICS ################
def graph_density(G):
    """ Returns density of the given graph"""
    return nx.density(G)

def graph_supernode_flow(G):
    """ Returns number of nodes that are reachable by the mining reward supernode"""
    if '-1' in G.nodes():
        BFS_tree = nx.bfs_tree(G,'-1')
        return len(BFS_tree.nodes())/len(G.nodes())
    elif -1 in G.nodes():
        BFS_tree = nx.bfs_tree(G, -1)
        return len(BFS_tree.nodes()) / len(G.nodes())
    else: return -1.0

def graph_diameter(G):
    """ Returns maximum diameter across each strongly connected component"""
    max_diam = 0
    for c in nx.strongly_connected_components(G):
        conn_subgraph = G.subgraph(c).copy()
        max_diam = max(max_diam, nx.diameter(conn_subgraph))
    return max_diam

def graph_SCC_orders(G):
    """ Returns list of SCC orders"""
    return [len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]

def graph_SCC_mean(G):
    """ Returns mean of SCC orders"""
    SCC_orders=graph_SCC_orders(G)
    return stats.mean(SCC_orders)

def graph_SCC_median(G):
    """ Returns median of SCC orders"""
    return stats.median(graph_SCC_orders(G))

def graph_SCC_max(G):
    """ Returns max of SCC orders"""
    return max(graph_SCC_orders(G))

def print_all_metrics(G):
    """
    Prints all metrics about graph
    :param G: Graph to judge metrics on
    """
    print("Density:",graph_density(G)*100,"%")
    print("Supernode flow: {:3.2f}%".format(graph_supernode_flow(G)*100))
    SCC = nx.strongly_connected_components(G)
    # max_diam = 0
    # for c in SCC:
    #     conn_subgraph = G.subgraph(c).copy()
    #     max_diam = max(max_diam, nx.diameter(conn_subgraph))
    # print("Diameter:", max_diam)
    SCC_orders = [len(c) for c in SCC]
    df= pd.DataFrame({'SCC_orders':SCC_orders})
    print( df.SCC_orders.value_counts().reset_index().rename(
           columns={'index': 'SCC Orders', 'SCC_orders': 'count'}).sort_values(by='SCC Orders', ascending=False))
    print("SCC Order Mean:", stats.mean(SCC_orders))
    print("SCC Order Median:", stats.median(SCC_orders))
    print("SCC Order Max:", max(SCC_orders))



import requests
import networkx as nx
import matplotlib.pyplot as plt


def download_latest_block_to_file(filename):
    """
    Download latest block to file
    :param filename: filename to write graph to
    """
    url = "https://blockchain.info/"

    G = nx.Graph()
    # fig = plt.figure(figsize=(7.656, 7.516))
    # plt.ion()
    plt.show(block=False)


    # Get latest block
    response = requests.get(url + "latestblock")
    if response.status_code == 200: # If request is successful, continue
        blockhash = response.json()['hash'] # Get blockhash
        response = requests.get(url + "rawblock/" + blockhash) # Request raw block data to get transactions
        if response.status_code == 200: # If request is successful, continue
            txs = response.json()['tx'] # Get list of transaction hashes
            num_txs = len(txs)
            counter =0
            print("num txs"+str(len(txs)))
            for tx in txs: # Iterate over each transaction
                counter +=1
                print(counter)
                response = requests.get(url + "rawtx/" + tx['hash']) # Request detailed transaction data
                if response.status_code == 200: # If request is successful, continue
                    input_addr = set() # empty input address sets
                    output_addr = set()
                    inputs = response.json()['inputs'] # Get input  data
                    outputs = response.json()['out']   # Get output data
                    for idx in range(len(inputs)): # Loop over inputs
                        try: input_addr.add(inputs[idx]['prev_out']['addr']) # If address present, add to input_addr set
                        except: input_addr.add(-1) # If address not present, add supernode to represent mining reward
                    # Add output addresses to output_addr. When several BTC chunks are given to the same address,
                    # the 'addr' property is not present, so we skip that address
                    [output_addr.add(outputs[idx]['addr']) for idx in range(len(outputs)) if ('addr' in outputs[idx].keys() and outputs[idx]['addr'] not in input_addr)]
                    # Make relabeling dictionary
                    lab_dict = dict()
                    idx = 0
                    for addr in input_addr:
                        lab_dict[idx] = addr
                        idx += 1
                    for addr in output_addr:
                        lab_dict[idx] = addr
                        idx += 1
                    # Make complete bipartite graph
                    CBG = nx.complete_bipartite_graph(len(input_addr), len(output_addr))
                    nx.relabel_nodes(CBG, lab_dict,False)
                    # Union G and CBG
                    G.add_nodes_from(CBG)
                    G.add_edges_from(CBG.edges())
    nx.write_adjlist(G, filename)

import requests # Gets website JSON information
import networkx as nx # Used for graphs
import json # Used to write to JSON file
import numpy as np # Used for adding arrays together
from varname import nameof

def analyze_blocks():
    """
    This function does analysis on the lastest n blocks
    """
    url = "https://blockchain.info/"
    n = 144 # Number of blocks to look at

    # We will be calculating the total number of transactions, maximum number in one block, and minimum in one block
    n_tx_counter=0
    max_n_tx = 0
    max_hash =0
    min_n_tx=3000
    min_hash = 0

    n_counter = n # Used to stop while loop
    # Get latest block
    response = requests.get(url + "latestblock")
    if response.status_code == 200:  # If request is successful, continue
        blockhash = response.json()['hash']  # Get blockhash
        height = str(response.json()['height'])
        response = requests.get(url + "rawblock/" + blockhash)  # Request raw block data to get transactions
        while n_counter>0:
            print(n_counter)
            if response.status_code == 200:  # If request is successful, continue
                blockhash = response.json()['prev_block']  # Get blockhash
                n_tx = response.json()['n_tx']
                n_tx_counter += n_tx
                max_n_tx = max(max_n_tx, n_tx)
                if n_tx==max_n_tx: max_hash=blockhash
                min_n_tx = min(min_n_tx, n_tx)
                if n_tx==min_n_tx: min_hash=blockhash

                response = requests.get(url + "rawblock/" + blockhash)  # Request raw block data to get transactions
            n_counter = n_counter - 1
        print("n:",n,"\nn_tx:",n_tx_counter,"\naverage tx per block: ", n_tx_counter/n,"\nmax: ", max_n_tx,
              "\nmax hash:", max_hash,"\nmin: ", min_n_tx, "\nmin hash:", min_hash)




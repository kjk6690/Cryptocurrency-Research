from draw_graph_from_file import *
from download_latest_block_to_file import *
from analyze_blocks import *
import json

analyze_blocks()

# download_latest_block_to_file()
# G = draw_graph_from_file('data/block_724784.adjlist', circular=True,create_using=nx.DiGraph)

# Read data from .json file
# with open('block_724371.json', 'r') as openfile:
#     # Reading from json file
#     json_object = json.load(openfile)
#
# print(json_object)
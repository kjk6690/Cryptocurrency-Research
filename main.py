from draw_graph_from_file import *
from download_latest_block_to_file import *
import json

download_latest_block_to_file()
G = draw_graph_from_file('block_724371.adjlist',circular=True)
max_deg = 0
max_deg_node = -2
for (node, deg) in G.degree():
    if max_deg<deg:
        max_deg=deg
        max_deg_node=node
print("node ", max_deg_node, " has the highest degree of ", max_deg)

# with open('block_724371.json', 'r') as openfile:
#     # Reading from json file
#     json_object = json.load(openfile)
#
# print(json_object)
import networkx as nx
import matplotlib.pyplot as plt

fig = plt.figure()
fig.canvas.draw()
fig.canvas.flush_events()
G = nx.read_adjlist('first_graph.adjlist')
print("Made G")
nx.draw_networkx(G, with_labels=False, node_size=1, linewidths=.5)
print("Drawn")
plt.show()
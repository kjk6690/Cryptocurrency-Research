import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_from_file(filename,circular=False,with_labels=False):
    """
    Given an adjacency list representation of a graph, draw the graph
    Note: May take a long time if Graph is large
    :param filename: filename of adjacency list
    :param circular: Plot in circular format. Will draw graph faster
    """
    plt.figure()
    G = nx.read_adjlist(filename)
    print("Made Graph")
    if circular:
        nx.draw_circular(G, with_labels=with_labels, node_size=2, linewidths=.5)
    else:
        nx.draw_networkx(G, with_labels=with_labels, node_size=2, linewidths=.5)
    print("Drawn")
    plt.show()
    return G
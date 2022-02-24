import networkx as nx
import matplotlib.pyplot as plt

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
        nx.draw_circular(G, with_labels=with_labels, node_size=2, linewidths=.5)
    else:
        nx.draw_networkx(G, with_labels=with_labels, node_size=2, linewidths=.5)
    print("Drawn")
    plt.show()
    return G
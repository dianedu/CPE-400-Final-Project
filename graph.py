# Class to hold the topology of the network and to aid in the simulation
import node
from node import *

#hmmm dictionary data structure may be useful for look up
class Graph():
    def __init__(self, nodes : set[Node], adjacency : list) -> None:
        self.net_nodes = nodes
        self.adjacency_matrix = [] #list of lists
        

    def __repr__(self) -> str:
        #not sure quite yet how to present
        pass

    def breadth_first_search(self) -> None: # hmm maybe better implemented for each node, then nodes have neighbors of node objects?
        pass

# for ease of testing
if __name__ == "__main__":
    nodes = set() # might change to a list later
    nodes.add(Node(1))
    nodes.add(Node(2))
    nodes.add(Node(3))
    nodes.add(Node(4))
    nodes.add(Node(5))

    adj_list = [[0,1,0,0,0],[1,0,0,1,0],[0,0,0,1,0],[0,0,1,0,1],[0,0,0,0,1]]
    g = Graph(nodes, adj_list)
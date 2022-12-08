# Class to hold the topology of the network and to aid in the simulation
import node
from node import *

#hmmm dictionary data structure may be useful for look up
class Graph():
    def __init__(self, num_nodes : int, adjacency : list) -> None:
        self.nodes = []
        for i in range(num_nodes):
            self.nodes.append(Node(i))

        self.adjacency_matrix = adjacency #list of lists
        for i, neighbors in enumerate(self.adjacency_matrix):
            for connection in neighbors:
                if connection == 1:
                    self.nodes[i].add_neighbor(self.nodes[connection])

    def __repr__(self) -> str:
        for n in self.nodes:
            print(n)

    def breadth_first_search(self) -> None: # hmm maybe better implemented for each node, then nodes have neighbors of node objects?
        pass

# for ease of testing
if __name__ == "__main__":
    adj_list = [[0,1,0,0,0],[1,0,0,1,0],[0,0,0,1,0],[0,0,1,0,1],[0,0,0,0,1]]
    g = Graph(5, adj_list)
    print(g)
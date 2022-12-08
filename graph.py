# Class to hold the topology of the network and to aid in the simulation
import node
from node import *

class Graph():
    def __init__(self, nodes : set[Node], adjacency : list) -> None:
        self.net_nodes = nodes
        self.adjacency_matrix = [] #list of lists

    def __repr__(self) -> str:
        #not sure quite yet how to present
        pass



# for ease of testing
if __name__ == "__main__":
    pass
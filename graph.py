# Class to hold the topology of the network and to aid in the simulation
import node
from node import *

#hmmm dictionary data structure may be useful for look up
class Graph():
    def __init__(self, num_nodes : int, adjacency : list[list[int]]) -> None:
        self.nodes = []
        for i in range(num_nodes):
            self.nodes.append(Node(i))

        self.adjacency_matrix = adjacency #list of lists
        for i, neighbors in enumerate(self.adjacency_matrix):
            for j,connection in enumerate(neighbors):
                if connection == 1:
                    self.nodes[i].add_neighbor(self.nodes[j])

    def __repr__(self) -> str:
        node = sorted(str(n) for n in self.nodes)
        return '\n'.join(node)

    def get_nodes(self) -> list[Node]:
        return self.nodes

    def get_adjacency_matric(self) -> list[list[int]]:
        return self.adjacency_matrix

    def change_adjaceny_matrix(self, matix : list[list[int]]):
        pass

    # this may be done by the broadcast method, which does bfs implicitly
    # def breadth_first_search(self) -> None: # hmm maybe better implemented for each node, then nodes have neighbors of node objects?
    #     pass

# for ease of testing
if __name__ == "__main__":
    adj_list2 = [[0,1,1,0,0,0,0,0,0,0],
                    [1,0,0,0,1,0,0,0,0,0],
                    [1,0,0,1,0,0,0,0,0,0],
                    [0,0,1,0,0,1,0,0,0,0],
                    [0,1,0,0,0,1,0,0,0,0],
                    [0,0,0,1,1,0,1,1,0,0],
                    [0,0,0,0,0,1,0,0,1,0],
                    [0,0,0,0,0,1,0,0,0,1],
                    [0,0,0,0,0,0,1,0,0,1],
                    [0,0,0,0,0,0,0,1,1,0]]
    g2 = Graph(10,adj_list2)
    print(g2,"\n")
    packet2 = RREQ_Packet(1,9,50)
    g2.get_nodes()[1].get_packet(copy.deepcopy(packet2))
    # print(g2.get_nodes()[1].get_cached_route(9))
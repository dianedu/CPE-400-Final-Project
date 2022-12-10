# Class to create each router and each router's information 
import packet
from packet import *

class Node():
    def __init__(self, name : int) -> None: 
        self.label = name # may consider changing to an str type, not entirely sure yet
        self.adjacency_list = [] # may make more sense to store as a set
        self.packet = None #might need to be a list -> queue of packets
        self.packets_received = dict()
        # dictionary to hold cached routes to each destination router

    def __repr__(self) -> str:
        return f"{self.label}: {[n.get_label() for n in self.adjacency_list]}"

    def set_adjacency(self, adjacent_nodes : list) -> None:
        self.adjacency_list = adjacent_nodes

    def get_adjacency(self) -> list:
        return self.adjacency_list

    def set_label(self, name : int) -> None:
        self.label = name
    
    def get_label(self) -> int:
        return self.label

    def add_neighbor(self, new_neighbor) -> None:
        self.adjacency_list.append(new_neighbor)
        self.adjacency_list.sort(key=Node.get_label)

    def get_cached_route(self, dest : int) -> list[int]:
        pass

    def broadcast_packet(self) -> None:
        if self.packet != None:
            for node in self.adjacency_list:
                node.get_packet()
        # need to test if this works

    def create_rreq_packet(self, src : int, dest : int, hop_count : int) -> RREQ_Packet:
        self.packet = RREQ_Packet(src, dest, hop_count)
        RREQ_Packet.generate_new_id()
        return self.packet # may not need this return

    def get_packet(self, packet : Packet) -> None:
        self.packet = packet

    def process_packet(self) -> None:
        if type(self.packet) == RREQ_Packet: #not entirely sure if this will work
            self.process_RREQ_packet()
        else:
            self.discard_packet()

    def process_RREQ_packet(self) -> None:
        self.packet.decrease_hop()
        if self.packet.get_target_address() == self.label:
            self.accept_packet()
        elif self.packet.get_hop_limit == 1:
            self.discard_packet()
        else:
            #check if packet with same src, dest, and packet id has already came it, if so discard
            # if not, all to rreq table and append own address to packet
            #then, broadcast to its neighbors
            pass
        
    def accept_packet(self) -> None:
        pass

    def discard_packet(self) -> None:
        self.packet = None #hmm not sure if this sufficent since packet is now lost in memory

    # method to update dictionary of cached routes
        # recursively get route if successful?
            # how to handle case when unsuccessful?
# for ease of testing
if __name__ == "__main__":
    n1 = Node(1)
    #print(n1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n1_neighbors = [n2,n3,n4,n5]
    n1.set_adjacency(n1_neighbors)
    print(n1) # oh, how interesting, each nodes have their neighbors as well... I wonder if it would be better to just have their labels?
    #n1.set_adjacency([n.get_label() for n in n1_neighbors]) # list comprehension <3
    #print(n1) # this may be better
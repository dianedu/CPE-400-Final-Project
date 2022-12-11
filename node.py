# Class to create each router and each router's information 
import packet
from packet import *
import copy

class Node():
    def __init__(self, name : int) -> None: 
        self.label = name # may consider changing to an str type, not entirely sure yet
        self.adjacency_list = [] # may make more sense to store as a set
        self.packet = None #might need to be a list -> queue of packets
        self.packets_received = dict()
        # dictionary to hold cached routes to each destination router

    def __repr__(self) -> str:
        return f"{self.label}: {[n.get_label() for n in self.adjacency_list]}"

    def set_adjacency(self, adjacent_nodes : list) -> None: #might not be used, but could be useful
        self.adjacency_list = adjacent_nodes

    def get_adjacency(self) -> list:
        return self.adjacency_list
    
    def get_label(self) -> int:
        return self.label

    def get_packets_recieved(self) -> dict:
        return self.packets_received

    def add_neighbor(self, new_neighbor) -> None:
        self.adjacency_list.append(new_neighbor)
        self.adjacency_list.sort(key=Node.get_label)

    # TO DO: to be implemented once broadcasting works
    def get_cached_route(self, dest : int) -> list[int]:
        pass

    def broadcast_packet(self, packet : Packet) -> None:
        if packet != None:
            # print(f"{self.label} is attempting to broadcast packet: {self.packet}\n")
            print(f"\n{self.label} is attempting to broadcast packet: {packet.get_id()}")
            # print(f"{self.packet} is broadcasted to {[n.get_label() for n in self.adjacency_list]}\n")
            print(f"{packet.get_id()} is broadcasted to {[n.get_label() for n in self.adjacency_list]}")
            for node in self.adjacency_list:
                if node.label not in packet.get_traversed_addresses():
                    # self.packet.add_traversed_address(self.label) # add elsewhere
                    node.get_packet(copy.deepcopy(packet))

    def get_packet(self, packet : Packet) -> None:
        print(f"Got to the get_packet() for {self.label}")
        if packet != None:
            # print(f"{self.label} has recieved packet {packet}\n")
            print(f"\n{self.label} has recieved packet {packet.get_id()}")
            self.process_packet(packet)

    def process_packet(self, packet: Packet) -> None:
        # print(f"{self.label} is processing packet {self.packet}")
        print(f"{self.label} is processing packet {packet.get_id()}")
        if type(packet) == RREQ_Packet:
            print(f"Packet of type RREQ is being process by {self.label}")
            self.process_RREQ_packet(packet)
        if type(packet) == RREP_Packet:
            pass
        else:
            self.discard_packet(packet)

    def process_RREQ_packet(self, packet : RREQ_Packet) -> None:
        if packet != None:
            packet.decrease_hop()
            if packet.get_target_address() == self.label:
                self.accept_RREQ_packet(packet)
            elif packet.get_hop_limit == 1:
                self.discard_packet(packet)
            else:
                packet_info = (packet.get_src(), packet.get_target_address())
                if self.is_in_rreq_table(packet_info, packet.get_id()):
                    self.discard_packet(packet)
                else:
                    packet.add_traversed_address(self.label) #might need to change
                    #self.packet = packet #need to put this somewhere.... hmm maybe only upon acceptance? and broadcast also takes in a packet
                    self.broadcast_packet(packet)
        
    # TO DO: Implement after cached route gets implemented
    def accept_RREQ_packet(self, packet : Packet) -> None:
        if not packet == self.packet:
            self.packet = packet
            print(f"{self.label} accepted packet {self.packet.get_id()}")
            print(self.packet.get_traversed_addresses())
        # otherwise a duplicate
        else:
            self.discard_packet(packet)

    def discard_packet(self, packet : Packet) -> None:
        print(f"Packet with id {packet.get_id()} is discarded by {self.label}")
        packet = None #hmm not sure if this sufficent since packet is now lost in memory

    # need to test and need potential refactoring
    def is_in_rreq_table(self, p_info : tuple, p_id :int) -> bool:
        print(f"Checking to see if packet has been processed by {self.label} previously")
        if p_info in self.packets_received.keys():
            if p_id in self.packets_received[p_info]:
                return True
            else:
                self.packets_received[p_info].append(p_id) # potential issue here
                return False
        self.packets_received[p_info] = [p_id] #need to figure out how to make the values a list
        return False

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
    print(n1)
# Class to create each router and each router's information 
import packet
from packet import *
import copy
import random

Successes = 0 # Variable to keep track of successful transmissions
Failures = 0 # Variable to keep track of unsuccessful transmissions

# The Node class represents each router in the network and its neighbors
class Node():
    # The Node class contructor requires a Node label for identification and the probability of each link's failure
    # The Node class constructor is invoked in the Graph class
    def __init__(self, name : int, prob_failure : float) -> None: 
        self.label = name #ID of router
        self.adjacency_list = [] # Neighbors of the router
        self.packet = None  # Packets accepted
        self.packets_received = dict() # RREQ table to check if received packet previously
        self.cached_routes = dict() # Table lookup of cached routes
        self.prob_link_failure = prob_failure

    def __repr__(self) -> str:
        return f"{self.label}: {[n.get_label() for n in self.adjacency_list]}"

    def set_adjacency(self, adjacent_nodes : list) -> None:
        self.adjacency_list = adjacent_nodes

    def get_adjacency(self) -> list:
        return self.adjacency_list
    
    def get_label(self) -> int:
        return self.label
    
    def get_prob_link_failure(self) -> float:
        return self.prob_link_failure

    def set_prob_link_failure(self, probability : float) -> None:
        self.prob_link_failure = probability

    def get_packets_recieved(self) -> dict:
        return self.packets_received

    def add_neighbor(self, new_neighbor) -> None:
        self.adjacency_list.append(new_neighbor)
        self.adjacency_list.sort(key=Node.get_label)

    # Method to get cached routes of previously reached destinations
    # @param    Address of destionation
    # @return   A list of Nodes to traverse to get to destination
    def get_cached_route(self, dest : int) -> list[int]:
        return self.cached_routes.get(dest)

    # Method to broadcast RREQ packets to neighbors
    # @param    Packet to be transmitted
    # @return   None
    def broadcast_packet(self, packet : Packet) -> None:
        if packet != None:
            # print(f"\n{self.label} is attempting to broadcast packet: {packet.get_id()}")
            # print(f"RREQ Packet {packet.get_id()} is broadcasted to {[n.get_label() for n in self.adjacency_list]}\n")
            for node in self.adjacency_list:
                if node.label not in packet.get_traversed_addresses():
                    node.get_packet(copy.deepcopy(packet))

    # Method get packet transmitted
    # @param    Packet received
    # @return   None
    def get_packet(self, packet : Packet) -> None:
        # print(f"{self.label} has received packet {packet.get_id()}")
        if packet != None:
            # print(f"\n{self.label} has recieved packet {packet.get_id()}")
            if type(packet) == RREQ_Packet:
                if packet.get_dest() in self.cached_routes.keys():
                    packet = self.convert_RREQ_to_Data_packet(copy.deepcopy(packet))
                    packet.set_route(self.cached_routes[packet.get_dest()])
            self.process_packet(copy.deepcopy(packet))

    # Upon getting packet, method to process the packet
    # @param    Packet to be processed
    # @return   None
    def process_packet(self, packet: Packet) -> None:
        # # print(f"{self.label} is processing packet {packet.get_id()}")
        if type(packet) == RREQ_Packet:
            self.process_RREQ_packet(packet)
        elif type(packet) == RREP_Packet:
            self.process_RREP_packet(packet)
        elif type(packet) == Data_Packet:
            self.process_Data_packet(packet)

    # Method to process RREQ packets
    # @param    Packet to processed
    # @return   None
    def process_RREQ_packet(self, packet : RREQ_Packet) -> None:
        if packet != None:
            packet.decrease_hop()
            if packet.get_dest() == self.label:
                self.accept_RREQ_packet(packet)
            elif packet.get_hop_limit == 1:
                self.discard_packet(packet)
            else:
                packet_info = (packet.get_src(), packet.get_dest())
                if self.is_in_rreq_table(packet_info, packet.get_id()):
                   self.discard_packet(packet)
                else:
                    packet.add_traversed_address(self.label)
                    self.broadcast_packet(packet)
        
    # Method accept RREQ packet and perform any required actions when accepted
    # @param    Packet to be accept
    # @return   None
    def accept_RREQ_packet(self, packet : Packet) -> None:
        if not self.packet == packet:
            self.packet = packet
            # print(f"{self.label} accepted packet {self.packet.get_id()}")
            # print(f"{self.label} is sending a RREP packet back\n")
            rrep_packet = RREP_Packet(self.label, self.packet.get_src(), 50)
            rrep_packet.set_addresses(copy.deepcopy(self.packet.get_traversed_addresses()))
            rrep_packet.set_route(copy.deepcopy(self.packet.get_traversed_addresses()))
            self.send_RREP_packet(rrep_packet)
        # otherwise a duplicate
        else:
            self.discard_packet(packet)

    # Method to discard packets
    # @param    Packet to be discarded
    # @return   None
    def discard_packet(self, packet : Packet) -> None:
        # print(f"Packet with id {packet.get_id()} is discarded by {self.label}")
        packet = None

    # Method to check if received same RREQ packet before
    # @param    Packet info
    # @return   Boolean to indicate if received or not
    def is_in_rreq_table(self, p_info : tuple, p_id :int) -> bool:
        if p_info in self.packets_received.keys():
            if p_id in self.packets_received[p_info]:
                return True
            else:
                self.packets_received[p_info].append(p_id)
                return False
        self.packets_received[p_info] = [p_id]
        return False

    # Method to send RREP packet
    # @param    Packet to send to destination
    # @return   None
    def send_RREP_packet(self, packet : RREP_Packet) -> None:
        destination = packet.get_route()[-1]
        packet.get_route().pop(-1)
        # print(f"RREP Packet {packet.get_id()} is being sent from {self.label} to {destination}")
        self.get_neighbor_node_from_label(destination).get_packet(packet)

    # Method to process RREP packets
    # @param    RREP Packet to process
    # @return   None
    def process_RREP_packet(self, packet : RREP_Packet) -> None:
        # print(f"RREP Packet {packet.get_id()} is being processed by {self.label}")
        if packet.get_dest() == self.label:
            self.accept_RREP_packet(packet)
        else:
            self.send_RREP_packet(packet)

    # Method to perform actions upon accepting RREP packets
    # @param    RREP packet accepted
    # @return   None
    def accept_RREP_packet(self, packet : RREP_Packet) -> None:
        # print(f"{self.label} accepted RREP packet with id: {packet.get_id()}\n")
        # print(f"Packet src: {packet.get_src()} and the packet addresses {packet.get_addresses()}")
        packet.get_addresses().pop(0)
        packet.get_addresses().append(packet.get_src())
        self.cached_routes[packet.get_src()] = packet.get_addresses()

    # Helper method to get neighbor Node from its label
    # @param    Neighbor node label
    # @return   Node of desired neighbor
    def get_neighbor_node_from_label(self, label : int):
        for node in self.adjacency_list:
            if label == node.get_label():
                return node

    # Helper method to send packet via cached route
    # @param    Packet to send to destination
    # @return   Data packet to send
    def convert_RREQ_to_Data_packet(self, packet : RREQ_Packet) -> Packet:
        return Data_Packet(packet.get_src(), packet.get_dest(), packet.get_hop_limit())

    # Method to process Data Packets
    # @param    Data Packet to process
    # @return   None
    def process_Data_packet(self, packet : Data_Packet) -> None:
        # print(f"{self.label} is processing Data Packet {packet.get_id()}")
        if packet.get_dest() == self.label:
            self.accept_Data_packet(packet)
        else:
            chance_fail = random.random()
            # print(f"Chance fail: {chance_fail} and the link failure rate {self.prob_link_failure}")
            next_hop_router = packet.get_route().pop(0)
            if chance_fail > self.prob_link_failure: 
                # print(f"next hop router in data packet sending: {next_hop_router}")
                self.get_neighbor_node_from_label(next_hop_router).get_packet(packet)
            else:
                print(f"Link from {self.label} to {next_hop_router} is broken")
                global Failures
                Failures += 1

    # Method to perform actions upon accepting a data packet via cached route
    # @param    Data Packet accepted
    # @return   None
    def accept_Data_packet(self, packet : Data_Packet) -> None:
        # print(f"{self.label} accepted Data Packet {packet.get_id()}")
        print(f"Packet is successfully transmitted")
        global Successes
        Successes += 1

def get_num_successes() -> int:
    return Successes

def get_num_failures() -> int:
    return Failures

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

    print("Testing random number generator")
    print(random.random())
    print(random.random())
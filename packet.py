# Class for DSR packets that are being transmitted

from abc import ABC, abstractmethod

# Abstract class for packet since the other DSR packets derive from it
class Packet(ABC):
    def __init__(self, source : int, destination : int, pack_type : str, optional = None) -> None:
        self.src = source 
        self.dest= destination
        self.type = pack_type
        self.opt = optional

    @abstractmethod
    def __repr__(self) -> str:
        pass

    def get_src(self) -> int:
        return self.src
    
    def get_dest(self) -> int:
        return self.dest

    def set_src(self, destination : int) -> None:
        self.dest = destination

    def get_pack_type(self) -> str:
        return self.type

# Class for RREQ packets
class RREQ_Packet(Packet):
    id_generator = 0
    def __init__(self, source : int, target : int, ttl : int) -> None:
        self.SRC = source
        self.hop_limit = ttl
        self.id = RREQ_Packet.id_generator
        self.dest = target
        self.addresses = []
        RREQ_Packet.generate_new_id()

    def __repr__(self) -> str:
        return f"RREQ Packet ID: {self.id}\nOriginal source: {self.SRC}\nTarget Destination: {self.dest}\nHop Limit: {self.hop_limit}"
    
    #Method to check if two RREQ packets are equal
    def __eq__(self, p : Packet) -> bool:
        if p == None:
            return False
        elif self.id == p.id:
            return True
        else:
            return False

    def get_src(self) -> int:
        return self.SRC

    def get_hop_limit(self) -> int:
        return self.hop_limit

    def decrease_hop(self) -> None:
        self.hop_limit -= 1

    def get_id(self) -> int:
        return self.id

    def get_dest(self) -> int:
        return self.dest

    # method for nodes to add own address to path the packet has traversed
    def add_traversed_address(self, address: int) -> None:
        self.addresses.append(address)

    def get_traversed_addresses(self) -> list[int]:
        return self.addresses

    @staticmethod
    def generate_new_id() -> None:
        RREQ_Packet.id_generator += 1

# Class for RREP packets
class RREP_Packet(Packet):
    id_generator = 0
    def __init__(self, source: int, destination: int, ttl : int) -> None:
        self.src = source
        self.dest = destination
        self.hop_limit = ttl
        self.id = RREP_Packet.id_generator
        self.addresses = None
        self.route = None
        RREP_Packet.generate_new_id()

    def __repr__(self) -> str:
       return f"RREP ID: {self.id}\nSource: {self.src}\nDestination: {self.dest}\nHop Limit: {self.hop_limit}"

    def get_src(self) -> int:
        return self.src
    
    def get_dest(self) -> int:
        return self.dest
    
    def get_hop_limit(self) -> int:
        return self.hop_limit

    def decrease_hop(self) -> None:
        self.hop_limit -= 1

    def get_id(self) -> int:
        return self.id
    
    def get_addresses(self) -> list[int]:
        return self.addresses

    def set_addresses(self, traversed_addressses : list[int]) -> None:
        self.addresses = traversed_addressses

    def get_route(self) -> list[int]:
        return self.route

    def set_route(self, traversed_addresses : list[int]) -> None:
        self.route = traversed_addresses

    @staticmethod
    def generate_new_id() -> None:
        RREP_Packet.id_generator += 1

#Class for Data_Packets to help with transmission via cached route
class Data_Packet(Packet):
    id_generator = 0
    def __init__(self, source: int, destination: int, ttl : int) -> None:
        self.src = source
        self.dest = destination
        self.hop_limit = ttl
        self.id = Data_Packet.id_generator
        self.route = list()
        Data_Packet.generate_new_id() 

    def __repr__(self) -> str:
        return f"Data Packet ID: {self.id}\nSource: {self.src}\nDestination: {self.dest}\nHop Limit: {self.hop_limit}"

    def get_src(self) -> int:
        return self.src
    
    def get_dest(self) -> int:
        return self.dest
    
    def get_hop_limit(self) -> int:
        return self.hop_limit

    def decrease_hop(self) -> None:
        self.hop_limit -= 1

    def get_id(self) -> int:
        return self.id

    def get_route(self) -> list[int]:
        return self.route

    def set_route(self, route_to_take : list[int]) -> None:
        self.route = route_to_take

    @staticmethod
    def generate_new_id() -> None:
        Data_Packet.id_generator += 1

# for testing purposes
if __name__ == "__main__":
    # TESTING RREQ_Packet class and its methods:
    p1 = RREQ_Packet(0, 4, 50)
    print(p1,"\n")
    p2 = RREQ_Packet(2, 4, 50)
    print(p2,"\n")
    p1.decrease_hop()
    print(p1,"\n")
    print(p1.get_traversed_addresses())
    p1.add_traversed_address(2)
    print(p1.get_traversed_addresses())
    p1.add_traversed_address(3)
    print(p1.get_traversed_addresses())
    #print(type(p2))

    #TESTING RREP_Packet class and its methods:
    p3 = RREP_Packet(4, 0, 50)
    print(p3,"\n")
    p4 = RREP_Packet(4, 2, 50)
    print(p4,"\n")
    p3.decrease_hop()
    print(p3,"\n")
    print(p4.get_addresses())
    p4.set_addresses([4,1,2,0])
    print(p4.get_addresses())
    p4.set_route([4,1,2,0])
    print(p4.get_route(),"\n")

    #TESTING Data_Packet class and its methods:
    p5 = Data_Packet(0, 4, 50)
    print(p5, "\n")
    p6 = Data_Packet(2, 4, 50)
    print(p6, "\n")
    p5.decrease_hop()
    print(p5, "\n")
    print(p6.get_route())
    p6.set_route([4, 6, 2, 1,0])
    print(p6.get_route())
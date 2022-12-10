# Class for DSR packets that are being transmitted

from abc import ABC, abstractmethod

# Abstract class for packet since the other DSR packets derive from it
class Packet(ABC):
    def __init__(self, source : int, destination : int, pack_type : str, optional = None) -> None:
        self.src = source 
        self.dest= destination
        self.type = pack_type
        self.opt = optional

    #not sure how this is going to work
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

    # @abstractmethod
    # def get_opt(self) -> None:
    #     pass

    # @abstractmethod
    # def set_opt(self, option=None) -> None:
    #     pass

# Class for RREQ packets
class RREQ_Packet(Packet):
    # def __init__(self, original_source: int, destination: int) -> None:
    #     super().__init__(original_source, destination, "RREQ", [])
    id_generator = 0
    def __init__(self, source : int, target : int, num_hops : int) -> None:
        self.SRC = source
        self.hop_limit = num_hops
        self.id = RREQ_Packet.id_generator
        self.target_address = target
        self.addresses = []

    def __repr__(self) -> str:
        return f"Packet ID: {self.id}\nOriginal source: {self.SRC}\nTarget Destination: {self.target_address}\nHop Limit: {self.hop_limit}"

    def get_src(self) -> int:
        return self.SRC

    def get_hop_limit(self) -> int:
        return self.hop_limit

    def decrease_hop(self) -> None:
        self.hop_limit -= 1

    def get_id(self) -> int:
        return self.id

    def get_target_address(self) -> int:
        return self.target_address

    # method for nodes to add own address to path the packet has traversed
    def add_traversed_address(self, address: int) -> None:
        self.addresses.append(address)

    def get_traversed_addresses(self) -> list[int]:
        return self.addresses

    @staticmethod
    def generate_new_id() -> None:
        RREQ_Packet.id_generator += 1

# TO DO
# # Class for RREP packets
# class RREP_Packet(Packet):
#     def __init__(self, source: int, destination: int, optional=None) -> None:
#         super().__init__(source, destination, "RREP", optional)

#     def __repr__(self) -> str:
#         # to come back to for implementation
#         # return super().__repr__()
#         pass

#     #to be continued implemented -- some logistics to figure out here

# TO DO
# # Class for RERR packets
# class RERR_Packet(Packet):
#     def __init__(self, source: int, destination: int, optional=None) -> None:
#         super().__init__(source, destination, "RERR", optional)

#     def __repr__(self) -> str:
#         # to come back to for implementation
#         # return super().__repr__()
#         pass

#     def get_opt(self) -> None:
#         print("Error occurred in routing, path to destination does not exist") #temporary

# for testing purposes
if __name__ == "__main__":
    p1 = RREQ_Packet(0, 50, 4)
    RREQ_Packet.generate_new_id()
    print(p1,"\n")
    p2 = RREQ_Packet(1, 50, 4)
    RREQ_Packet.generate_new_id()
    print(p2)
    print(type(p2))

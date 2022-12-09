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

    def set_src(self, source : int) -> None:
        self.src = source
    
    def get_dest(self) -> int:
        return self.dest

    def set_src(self, destination : int) -> None:
        self.dest = destination

    def get_pack_type(self) -> str:
        return self.type

    @abstractmethod
    def get_opt(self) -> None:
        pass

    @abstractmethod
    def set_opt(self, option=None) -> None:
        pass

# Class for RREQ packets
class RREQ_Packet(Packet):
    def __init__(self, original_source: int, destination: int) -> None:
        super().__init__(original_source, destination, "RREQ", [])

    def __repr__(self) -> str:
        # to come back to for implementation
        # return super().__repr__()
        pass

    def get_opt(self) -> None:
        if self.opt == None:
            print("RREQ Packet has nothing in its options field") # might need to comment out later
            return None
        else: 
            return self.opt # this might not be helpful thinking about it now

    def set_opt(self, option=None) -> None: # might not need this method (safer without)
        self.set_opt = option

    def add_opt(self, option) -> None:
        self.opt.append(option) #self.opt should be a list to hold all the paths traversed




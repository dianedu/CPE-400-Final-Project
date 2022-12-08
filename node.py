# Class to create each router and each router's information 

class Node():
    def __init__(self, name : int) -> None: 
        self.label = name # may consider changing to an str type, not entirely sure yet
        self.adjacency_list = [] # may make more sense to store as a set
        # dictionary to hold cached routes to each destination router

    def __repr__(self) -> str:
        # might need to modify later
        return f"{self.label}: {self.adjacency_list}"

    def set_adjacency(self, adjacent_nodes : list) -> None:
        self.adjacency_list = adjacent_nodes

    def get_adjacency(self) -> list:
        return self.adjacency_list

    def set_label(self, name : int) -> None:
        self.label = name
    
    def get_label(self) -> int:
        return self.label

    def get_cached_route(self, dest : int) -> list[int]:
        pass

    # method to update dictionary of cached routes
        # recursively get route if successful?
            # how to handle case when unsuccessful?
# for ease of testing
if __name__ == "__main__":
    n1 = Node(1)
    print(n1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n1.set_adjacency([n2,n3,n4,n5])
    print(n1) # oh, how interesting, each nodes have their neighbors as well... I wonder if it would be better to just have their labels?
    n1_neighbors = [n2,n3,n4,n5]
    n1.set_adjacency([n.get_label() for n in n1_neighbors]) # list comprehension <3
    print(n1) # this may be better
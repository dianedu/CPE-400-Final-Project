# Main file to run for the simulation for the CPE 400 Final Project
# CPE 400 - Final Project
# Diane Du, Kalista Hong, Abida Mim
# December 12, 2022

import graph
from graph import *
import node
from node import *

# main function for simluation
if __name__ == "__main__":
    probability_of_link_failure = 0.5

    # TEST 1:
    adj_list1 = [[0,1,1,0,0],
                [1,0,0,1,0],
                [1,0,0,1,0],
                [0,1,1,0,1],
                [0,0,0,1,0]]
    g1 = Graph(5, adj_list1, probability_of_link_failure)
    packet1 = RREQ_Packet(0, 4, 50)
    g1.get_nodes()[0].get_packet(packet1)
    cache_packet1 = RREQ_Packet(0, 4, 50)

    for i in range(100):
        g1.get_nodes()[0].get_packet(copy.deepcopy(cache_packet1))

    print(f"\nSuccess: {get_num_successes()}, Failures: {get_num_failures()}, Prob link Failure: {probability_of_link_failure}")
    print(g1,"\n")
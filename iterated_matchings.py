from matching_complexes import *
import networkx as nx

#edge_list = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)] #C5
#edge_list = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (5, 6)] #K4 disun edge
#edge_list = [(1, 5), (2, 5), (3, 5), (4, 5), (8, 6), (7, 6)] #S4 disun S2
#edge_list = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 6)] #C5 with a pendant
#edge_list = [(1,3), (3, 2), (3, 5), (5,4), (5, 6), (6, 7)] #P4 plus two pendants on adjacent vertices
#edge_list = [(1,2), (2, 3), (3,4), (4, 5), (3, 6)] #P4 plus one pendant on middle vertex
#edge_list = [(1,2), (2, 3), (3,4), (4, 5), (2, 6)] #P4 plus one pendant on second vertex
#edge_list = [(1,2), (2, 3), (2, 4), (4, 5), (3, 5), (1, 5), (5, 6)]
#edge_list = [(1, 2), (2, 3), (2, 6), (2, 4), (4, 5)] #P3 with two pendants (2,2- dimethalbutane)
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (4, 6)] #P3 with two pendants (2,3- dimethalbutane)
#edge_list = [(1, 2), (2, 3), (2, 4), (2, 5), (5, 6)] #(2,2-dimenthalpropane)
#edge_list = [(1, 3), (3, 2), (3, 4), (4, 5), (5, 6), (5, 7)] #P4 with two pendants
#edge_list = [(1, 3), (3, 2), (2, 1), (5, 4), (6, 7)]
#edge_list = [(1, 5), (2, 5), (3, 5), (4, 5), (6, 8), (7, 6)] #S4 disun S2
#edge_list = [(1, 2), (1, 4), (1, 5), (2, 6), (2, 3), (3, 7), (3, 4), (4, 8), (5, 8), (5, 6), (6, 7), (7, 8)] #3D cube
#edge_list = [(1,2), (2,3), (3,4), (4,5), (5,6), (6,1), (2, 7), (4, 8), (6, 9)] # C_6 plus 3 pendants

#These are the edge lists for 5 different graphs with 5 vertices and 5 edges
#edge_list = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)] #C5
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5)] #C4 with pendent
#edge_list = [(1, 2), (2, 3), (3, 4), (2, 4), (4, 5)] #C3 with two pendents on adjacent vertices
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (3, 5)] #C3 with two pendents on same vertex
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5)] #C3 with a P2
edge_list = [(1, 2), (2, 3), (3, 4), (4, 6), (3, 5), (5, 6)] #C4 with P2
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6)] #C3 with a P3

#These are the possible graphs with 6 edges and a diameter of 3 (that I needed a program to check)
#edge_list = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (5, 6)] #C3 with pendant and P2 on a vetex
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (3, 5), (2, 6)] #C3 with one pendant on one vertex and two pendents on another
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (4, 6)] #C3 with a S3 attached at leaf
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (1, 4)] #C4 with pendent and diagonal
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (4, 6), (4, 7)] #P3 with two pendants (2,3- dimethalpropane)
#edge_list = [(1, 2), (2, 3), (2, 4), (2, 5), (5, 6), (2, 7)] #(2,2,2-trimenthalpropane)
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (2, 6)] #C4 with two pendents on same vertex
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (4, 6)] #C4 with two pendents on adjacent vertices

#These are the possible graphs with 7 edges and a diameter of 3 that I needed to test
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (2, 5), (3, 6)] #C4 with P2 and diagonal
#edge_list = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (5, 6), (2, 7)] #C3 with two pendants and P2 on a vetex
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (2, 5), (5, 6)] #C4 with diagonal and pendants on opposite vertices
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (3, 5), (2, 6), (2, 7)] #C3 with two pendants on two vertices

to_draw = True
it = 5
vertices_count = list([])
edge_count = list([])

#implementation
#==========================================================================================================

#This is the main method for calling all of the stuff
def iterate_matching(edge_list, it, to_draw, vertices_count, edge_count):
    edges = edge_list

    #created the original graph using the "networksx" graph object
    G = nx.Graph()
    G.add_edges_from(edges)
    edge_labels = {e: i + 1 for i, e in enumerate(G.edges())}
    vertices_count.append(G.order())
    edge_count.append(G.size())

    #draws the original graph if drawing is desired
    if to_draw:
        # draws the graph given by edge list
        print("Drawing the graph...")
        draw_graph(G, edge_labels=edge_labels)

    for x in range(it): #executes the matching operation 'it' times
        print("Working on matching ", x)
        t = find_matching(G, edge_labels, to_draw)
        G = t[0]
        edge_labels = t[1]

        # adds the number of vertices to the list of vertex data
        #adds the number of edges to the list of edge data
        vertices_count.append(G.order())
        edge_count.append(G.size())

def find_matching(G, edge_labels, to_draw):
    #creating the graph from the edge list

    print("Calculating Matching...")
    maximal_matchings = skel_matching(G, edge_labels) #calls method from 'matching_complexes' program
    print("     Matching Complex is :", maximal_matchings)

    M_G = nx.Graph()
    M_G.add_edges_from(maximal_matchings)
    M_edge_labels = {e: i + 1 for i, e in enumerate(M_G.edges())}

    if to_draw:
        # draws the graph given by edge list
        print("Drawing the picture..." )
        draw_graph(M_G, edge_labels=M_edge_labels)

    return (M_G, M_edge_labels)

#=========================================================================================================
#      Main calls and stuff
#==========================================================================================================
iterate_matching(edge_list, it, to_draw, vertices_count, edge_count)

print(vertices_count)
print(edge_count)
print("done!")

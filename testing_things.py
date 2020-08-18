from matching_complexes import*

#These are the edge lists for 5 different graphs with 5 vertices and 5 edges
edge_list = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)] #C5
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5)] #C4 with pendent
#edge_list = [(1, 2), (2, 3), (3, 4), (2, 4), (4, 5)] #C3 with two pendents on adjacent vertices
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (3, 5)] #C3 with two pendents on same vertex
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5)] #C3 with a P2

#These are the possible graphs with 6 edges and a diameter of 3
#edge_list = [(1, 2), (2, 3), (3, 4), (2, 4), (4, 5), (5, 6)] #C3 with pendant on one vertex, P2 on another
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (3, 5), (2, 6)] #C3 with one pendant on one vertex and two pendents on another
#edge_list = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (4, 6)] #C3 with a S3 attached at leaf
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (5, 2)] #C4 with pendent and diagonal
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (4, 6), (4, 7)] #P3 with two pendants (2,3- dimethalpropane)
#edge_list = [(1, 2), (2, 3), (2, 4), (2, 5), (5, 6), (2, 7)] #(2,2,2-trimenthalpropane)
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (2, 6)] #C4 with two pendents on same vertex
#edge_list = [(1, 2), (2, 3), (2, 4), (4, 5), (1, 5), (4, 6)] #C4 with two pendents on adjacent vertices

edges = edge_list

# created the original graph using the "networksx" graph object
G = nx.Graph()
G.add_edges_from(edges)
edge_labels = {e: i + 1 for i, e in enumerate(G.edges())}

for edge in G.edges():
    for e2 in G.edges():
        if not((edge[0] in e2) or (edge[1] in e2)) :
             print(edge, " is not adjacent to", e2)

#maximal_matchings = skel_matching(G, edge_labels)  # calls method from 'matching_complexes' program
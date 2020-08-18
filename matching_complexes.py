'''

A variety of helpful functions for finding and plotting the matching complexes
of given graphs. These can be imported into another python file to use,
or at the bottom of this file you can use the main method to just
specify the graph in this file directly and just run this python file.

'''


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import more_itertools as mitl
import itertools as itl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import copy
import os
import shutil
import matplotlib.animation as manimation

def draw_graph(G, edge_labels=None):
    """
    Draws the given graph, using the spring-force algorithm to determine location of nodes.

    @params
        G = graph to be drawn (a networkx Graph object)
        edge_labels : dictionary mapping each edge to a name
    """
    pos=nx.spring_layout(G)
    nx.drawing.nx_pylab.draw(G, pos)
    if not edge_labels is None:
        nx.drawing.nx_pylab.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title('Graph G')
    plt.show()


# TODO: implement more efficient algorithm for finding matching.
def find_matching_complex(G, edge_labels=None):
    """
    Finds the matching complex of a given graph G

    @params
                  G = networkx graph object storing the graph to find a matching complex of. To create this from an
                      edge list, simply do:
                            G = networkx.Graph()
                            G.add_edges_from(edge_list)
                            
        edge_labels = List of names to give each of the edges in the matching.

    @returns
        maximal_matchings = A list of tuples for each face in the matching complex. e.g. a 1-tuple specifies a vertex, a 2-tuple an edge,
                            a 3-tuple a triangle, a 4-tuple a tetrahedron, etc
    """
    if edge_labels is None:
        edge_labels = {e: e for e in enumerate(G.edges())}

    matchings = set([])

    # find all possible matchings: improve this code if necessary

    for edge_set in mitl.powerset(G.edges()):
        if nx.algorithms.matching.is_matching(G, edge_set):
            matchings.add(tuple([edge_labels[e] for e in edge_set]))

    maximal_matchings = set() 
    for match in matchings:
        to_remove = set()
        for max_match in maximal_matchings:
            if set(match).issubset(set(max_match)): break
            if set(max_match).issubset(set(match)): to_remove.add(max_match)
        else:
            maximal_matchings.add(match)

        maximal_matchings = maximal_matchings - to_remove

    return maximal_matchings

#TODO: see if this program actually works
def skel_matching (G, edge_labels=None):
    '''
        This finds the 1-skeleton of the matching of a given graph.
        Same parameters and return as find_matching_complex
    '''
    if edge_labels is None:
        edge_labels = {e: e for e in enumerate(G.edges())}

    matchings = set([])
    toLook = list(G.edges())
    toCheck = list(G.edges())

    for e1 in toLook:
        toCheck.remove(e1)
        for e2 in toCheck:
            if not ((e1[0] in e2) or (e1[1] in e2)):
                matchings.add((edge_labels[e1], edge_labels[e2]))

    # find all possible matchings: improve this code if necessary
    # for edge_set in mitl.powerset(G.edges()):
    #     if len(edge_set) == 2:
    #         if nx.algorithms.matching.is_matching(G, edge_set):
    #             matchings.add(tuple([edge_labels[e] for e in edge_set]))


    return matchings

def draw_2D_matching_complex(M_G, fill=[]):
    """
    Draws the given matching complex in 2 dimensions, filling in any faces (e.g. triangles). Uses the spring-force
    algorithm to determine the location of nodes.

    @params
        M_G : matching complex; iterable of 2-tuples specifying each edge in the complex
        fill : tuples of vertices specifying a face to be colored. For example, (1,2,3) specifies coloring in the face made by
               vertices 1,2,3 (and the corresponding edges between them).
    """
    pos = nx.spring_layout(M_G, dim=2, iterations=100)

    nx.drawing.nx_pylab.draw(M_G, pos)
    nx.drawing.nx_pylab.draw_networkx_labels(M_G, pos)

    ax = plt.gca()
    for V in fill:
        x = [pos[v][0] for v in V]
        y = [pos[v][1] for v in V]
        ax.fill(x,y, "blue", alpha=0.2)


    plt.show()

def draw_3D_matching_complex(M_G,fill=[], k=None, iterations=100, make_video=False, vid_elevation=10, vid_path=None):
    """
    Draws the given matching complex in 3 dimensions, filling in any faces (e.g. triangles/tetrahedron). Uses the spring-force
    algorithm to determine the location of nodes.

    @params
           M_G : matching complex; iterable of 2-tuples specifying each edge in the complex
          fill : tuples of vertices specifying a face to be colored. For example, (1,2,3) specifies coloring in the face made by
                 vertices 1,2,3 (and the corresponding edges between them).
             k : optimal distance for nodes to be in graph. Allows you to adjust how far apart nodes are in drawing
    iterations : number of iterations to run stochastic spring-force algorithm for
    make_video : makes a video spinning simplicial complex around.
    vid_elevation : elevation of viewpoint when making video.
    vid_path : filepath to save video at

    @returns
        fig : returns matplotlib figure.
    """

    pos = nx.spring_layout(M_G, dim=3, k=k, iterations=iterations, weight="weight")

    fig = plt.figure()
    ax = fig.add_subplot('111', projection='3d')

    tetra_verts = []
    tri_verts = []
    for V in fill:
        verts = [tuple(pos[v]) for v in V]
        
        if len(verts) == 3: #triangle
            tri_verts.append(verts)
        elif len(verts) == 4: # tetrahedron
            for v1, v2, v3 in itl.combinations(verts, 3):
                tetra_verts.append((v1,v2,v3))


    poly = Poly3DCollection(tri_verts, linewidth=1, alpha=0.2)
    poly.set_facecolor('g')
    ax.add_collection3d(poly)
    poly = Poly3DCollection(tetra_verts, linewidth=1, alpha=0.2)
    poly.set_facecolor('b')
    ax.add_collection3d(poly)


    for key in pos:
        point = pos[key]
        ax.scatter(point[0], point[1], point[2], s=120, c='r', alpha=0.4, edgecolor='k')
        ax.text(point[0], point[1], point[2], key, fontsize=15) #horizontalalignment='center', verticalalignment='center')


    for e in M_G.edges():
        ax.plot(xs=[pos[e[0]][0], pos[e[1]][0]], ys=[pos[e[0]][1], pos[e[1]][1]], zs=[pos[e[0]][2], pos[e[1]][2]], c='k') 


    #### make a video out of stuff
    if make_video:
        writer = manimation.writers['ffmpeg'](fps=15)
        fig = plt.gcf()
        dpi = 200
        with writer.saving(fig, vid_path, dpi):

            # do stuff
            for ii in range(0,360,1):
                ax.view_init(elev=vid_elevation, azim=ii)
                writer.grab_frame()
            #### #############

    plt.show()

    return fig

        


        


    
def make_matching_complex(maximal_matchings, tetra_weight=1, tri_weight=1, other_weight=1):
    """
    Makes a networkx graph object for the given matching complex, assigning weights to the given edges based on what
    kind of face they reside in. These weights are used in determining the spring constants used in the spring-force
    algorithm to draw the graph, so assigning a higher weight to a given collection of faces will make it "more important" 
    those kinds of vertices are close together.

    @params
        maximal_matchings = matching complex; a series of tuples specifying matchings in graph (e.g. (1,2,3) specifies that edges 1,2,3 were
                            a valid matching in the graph). 
        tetra_weight = weight to give edges in tetrahedron faces
        tri_weight = weight to give edges in triangle faces
        other_weight = weight to give edges not part of higher dimensional faces (e.g. matchings of size 2, so just plain edges)

    @returns
        M_G = matching complex (networkx Graph object) with edge weights specified from above parameters
        fill = faces in graph that should be filled in with color (e.g. so higher dimensional faces like triangles/tetrahedron can be
                drawn on top of the edges of just the normal graph)
    """

    M_G = nx.Graph()
    fill = []
    for match in maximal_matchings:
        if len(match) == 3:
            for v1, v2 in itl.combinations(match, 2):
                M_G.add_edge(v1, v2, weight=tri_weight)
            fill.append(match) 

        elif len(match) == 4:
            for v1, v2 in itl.combinations(match, 2):
                M_G.add_edge(v1, v2, weight=tetra_weight)
            fill.append(match) 

        elif len(match) == 2:
            M_G.add_edge(match[0], match[1], weight=other_weight)

    return M_G, fill

# TODO: fix code for non simple graphs.
def graph_from_complex(faces, simple_graph=False):
    """
    Given a matching complex, find a graph that generates it (this graph may not be unique).

    @params
         faces : edges and higher dimensional faces of matching complex. Specified as a list of n-tuples of vertices.
                 for example, the 2-tuple (1,2) would specify an edge between vertices 1 and 2,
                 the 3-tuple (1,2,3) would specify a face between vertices 1,2,3 of M_G (e.g. a filled
                 in triangle). Similarly, a 4-tuple (1,2,3,4) would form a filled in tetrahedron between vertices 1,2,3,4

        simple_graph : Look for a simple graph (True/False) that generates this matching complex


    @returns
                  G : a networkx Graph object for a graph that generates this matching complex (if possible)
        edge_labels : dictionary mapping edges (v1, v2)  to edge labels (e.g. edge number)
    """
    vertices = list(set([x for face in faces for x in face]))

    # create adjacency lists for the edges of G
    # stores which edges in G have to be adjacent based on the structure of M_G
    adj_list = {v:set(vertices.copy()) for v in vertices}
    for v in vertices: adj_list[v].remove(v)
    
    # NOTE: Edges in G cannot be adjacent if their corresponding vertices are adjacent in M_G
    # or share a higher dimensional face.
    for f in faces:
        for v1, v2 in itl.combinations(f,2):
            try:
                adj_list[v1].remove(v2)
            except:
                pass

            try:
                adj_list[v2].remove(v1)
            except:
                pass

    
    # This will be the edge adjacency list for the graph G who generates this matching complex
    # namely, it will be a dictionary mapping each vertex to the set of edges adjacent to it.
    vertex_adj_list = {}

    # graph is a map from each vertex to the set of edges adjacent to it
    graph = helper(0, vertex_adj_list, adj_list, vertices, None, simple_graph)


    if graph is None:
        raise ValueError("The given complex is not the matching complex of some graph")
        
    # reconstruct the graph from the vertex_adj_list stored in graph.
    edge_map = {} # map from each edge to its two vertices
    for v in graph:
        for e in graph[v]:
            if e in edge_map:
                edge_map[e].add(v)
            else:
                edge_map[e] = set([v])

    if simple_graph:
        edge_labels = {tuple(edge_map[e]):e for e in edge_map}
        edge_list = edge_labels.keys()
    else:
        edge_list = [tuple(edge_map[e]) for e in edge_map]
        edge_labels = {}
        for e in edge_map:
            key = tuple(edge_map[e])
            if key in edge_labels:
                edge_labels[key] += [e]
            else:
                edge_labels[key] = [e]

    G = nx.Graph()
    G.add_edges_from(edge_list)

    print("edgelist: ", edge_list)

    return G, edge_labels

# NOTE: is it important an edge is not considered adjacent to itself?
def helper(index, vertex_adj_list, edge_adj_list, edges, first_vertex, simple_graph):
    '''
        helper method for graph_from_complex above

        @params
            index : current index in edge list we are considering. e.g. which edge are we trying to place
            vertex_adj_list : map from vertices (in G) to the edges (in G) they are adjacent to (currently. we are building this up)
            edge_adj_list : map from edges (in G) to edges (in G) they are adjacent to. This info was gathered from the matching complex
            first_vertex : For each edge, we have to assign both its endpoints to vertices in G. If one endpoint has already been assigned,
                           this stores the endpoint it was assigned to. This is None if no endpoints have been assigned yet.
            simple_graph : whether to allow multiple edges in the graph that generates G. Self-loops are ignored already as they dont affect matching complex.
    '''

    # We found a suitable graph!
    if index >= len(edges):
        return vertex_adj_list

    next_edge = edges[index]

    # What edges (that have already been placed) this current edge needs to be adjacent to
    needed_edges = set(filter(lambda x: edges.index(x) < index, edge_adj_list[next_edge]))
    if first_vertex is not None:
        needed_edges = needed_edges - vertex_adj_list[first_vertex]

    for v in vertex_adj_list:

        # if this edge is adjacent to all the edges already adjacent to the given vertex,
        # we can add it to the given vertex and recurse.
        if (first_vertex is None and vertex_adj_list[v] <= needed_edges) or (needed_edges == vertex_adj_list[v]): #TODO: Change this to be == needed edges if first vertex already chosen?

            # TODO: verify this simple graph check works properly.
            # Don't want to create a double edge if this is a simple graph
            if first_vertex is None or not simple_graph or len(vertex_adj_list[v].intersection(vertex_adj_list[first_vertex])) == 0:

                new_adj_list = copy.deepcopy(vertex_adj_list)
                new_adj_list[v].add(next_edge)


                if first_vertex is not None:
                    # just placed both vertices for current edge, so we can move on to the next edge
                    graph = helper(index + 1, new_adj_list, edge_adj_list, edges, first_vertex=None, simple_graph=simple_graph)
                else:
                    # only placed first vertex for current edge. Now we must place second vertex.
                    graph = helper(index, new_adj_list, edge_adj_list, edges, first_vertex=v, simple_graph=simple_graph)

                # lower branch found a solution!
                if graph is not None: return graph


    # This tries to handle the case where a given edge is incompatible with the current graph being built
    # Namely, if I can find edges that are adjacent to the edge I am currently trying to place, and this
    # edge is n. Note we have already placed edges with index less than the current edge
    #needed_edges = set(filter(lambda x:  edges.index(x) < index, edge_adj_list[next_edge])) # filter to consider only edges that have already been placed

    # Since there are edges the current edge is adjacent to that have already been placed,
    # I should have been able to find a compatible vertex to attach this edge to. Thus, the current
    # graph does not work so recurse upwards.

    # OR

    # Since there are edges the current edge is adjacent to that have already been placed AND that it is not already adjacent to,
    # I should have been able to find a compatible vertex to attach this edge to. Thus, the current
    # graph does not work so recurse upwards.

    if len(needed_edges) > 0: return None


    # else I have not found any vertices that I could attach this edge to, but none of the currently placed edges
    # need to be adjacent to this edge and currently aren't. So I am free to create a new vertex for one of this
    # current edge's endpoints
    new_adj_list = copy.deepcopy(vertex_adj_list)
    new_adj_list[len(vertex_adj_list)] = set([next_edge])

    if first_vertex is None:
        new_adj_list[len(vertex_adj_list) + 1] = set([next_edge])

    return helper(index + 1, new_adj_list, edge_adj_list, edges, first_vertex=None, simple_graph=simple_graph)



# ====================================================================================================================================

# NOTE: If you prefer, you can just run this file and specify graphs here

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="finding and drawing the matching complex for the given graph")
    #parser.add_help()
    parser.add_argument('-g', '--find_graph', action='store_true', default=False, help="find the a graph that generates given matching complex")
    parser.add_argument('-m', '--find_matching', action='store_true', default=False, help="find the matching complex of a given graph")
    parser.add_argument('--iterations', type=int, default=100, help="Number of iterations to run spring-force algorithm for")
    parser.add_argument('--opt_dist', type=float, default=None, help="Optimal distance between nodes in drawn graph. Can help spread out graphs.")
    parser.add_argument('--draw_2D', action='store_true', default=False, help="Draw matching complex in 2D rather than 3D")
    parser.add_argument('-w', '--weights', nargs=3, default=(1,1,1), help="Strength of edges for tetrahedron, triangle, and normal edges in matching complex.")

    args = parser.parse_args()


    if args.find_matching:
        # NOTE: Define graph as edge list  ================================================================

        '''
        This is where you can specify the graph G you want to find the matching complex of.
        Specify it as an edge list. Some examples can be found below.
        '''


        #edge_list = [(1,2), (2,3), (3,4), (1,4), (1,3), (2,4)] # K_4
        #edge_list = [(1,2), (2,3), (3,4), (4,5), (5,6), (6,1)] # C_6
        edge_list = [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,1)] # C_7
        #edge_list = [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,1)] # C_8
        #edge_list=[(1,2), (3,4), (5,6), (7,8)] # 4 disjoint edges
        #edge_list=[(1,2), (3,4), (5,6), (7,8)] # 4 disjoint edges
        
        
        # K_k,n
        '''
        k=4
        n=3
        edge_list =[]
        for i in range(k):
            for j in range(k, k+n):
                edge_list.append((i,j))
        '''


        #K_n
        '''
        n=6
        edge_list=[(i,j) for i,j in itl.combinations(list(range(n)), 2)]
        '''

        # ============================================================================================

        G = nx.Graph()
        G.add_edges_from(edge_list)

        edge_labels = {e:i+1 for i,e in enumerate(G.edges())}

        # draw the graph given by edge list
        draw_graph(G, edge_labels=edge_labels)

        maximal_matchings = find_matching_complex(G, edge_labels)

        print("Matching Complex is :", maximal_matchings)

        max_dim = max([len(m) for m in maximal_matchings])
        

        if max_dim > 4:
            print("Cannot draw matching complex. Simplicial complex dimension is > 3")
        elif max_dim == 1 or max_dim == 0:
            print("Matching complex is trivial.")
        else:
            M_G, fill = make_matching_complex(maximal_matchings, tetra_weight=args.weights[0], tri_weight=args.weights[1], other_weight=args.weights[2])

            if args.draw_2D:
                draw_2D_matching_complex(M_G,fill)

            else:
                draw_3D_matching_complex(M_G,fill, k=args.opt_dist, iterations=args.iterations)

        print("done!")


# =====================================================================================================

    # NOTE: Find the graph that generates a given matching complex.
    if args.find_graph:

        # NOTE: edit the following variables to specify your matching complex ===============================
        # labels to give vertices in M_G
        vertices = list(range(1,6))

        # edges in matching complex (NOT higher dimensional faces; simply specify the one-skeleton here)
        edges = [(1,2), (2,3), (3,4), (4,5), (5,1)]

        # Specify higher dimensional faces here as a list of tuples. For example, the 4-tuple
        # (1,2,3,4) would specify a filled in tetrahedron between vertices 1,2,3,4 in the matching complex
        faces = []

        #=====================================================================================================

        G = graph_from_complex(edges, vertices, faces)
        draw_graph(G, edge_labels=vertices)


# Matching Complex
For a graph G, a matching of G is a set of edges {e_1,... e_j} such that no edges in the set share an endpoint. The matching complex of a graph is the set of all matchings. This can be realized visually as a Simplicial Complex. For information on the math, check out *insert some stuff... link to paper?*.  

# This code
Here are some programs that will allow the user to calculate and draw matching complexes of any graph. Included are programs to find the matching complex from the graph, find the graph from the matching complex, calculate iterated matchings, and find the Line graph of a given graph.

Most of this code base was written by Zack Mcnulty: https://github.com/zackmcnulty


### Code Instructions

First, start off by cloning this repository using git. Essentially, you just need to download git (software) from the internet
and run `git clone https://github.com/zackmcnulty/WXML.git` in the terminal/command-line. This will create a folder in your local
directory and you can access the code there. Also run `pip install -r requirements.txt` in the command line to download all the 
python libraries I use in this code.

I have tried to make this code as accessible as possible. The main functions provided here is findind/drawing matching complex
given a graph G AND finding a graph that generates a given matching complex. All of the primary functions are found in the file
`matching_complexes.py` but I have also created some helper scripts `find_complex_from_graph.py` and `find_graph_from_complex.py` 
which have the obvious uses. In these helper files, you just need to specify some needed information (e.g. the edge list for the graph or
the matching complex) and run them: they will do the rest. 

If you want more flexibility in what you do, take a look at `matching_complexes.py`. You can import its methods into another python file
and use them as you wish.

Side note: I also created a script `linegraph.py` that plots the line graph of a given graph (specified in the file itself) if you find this useful.

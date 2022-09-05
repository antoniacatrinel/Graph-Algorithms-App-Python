# Graph Algorithms App

Create a **menu-driven console application** with the following operations:
- read the graph from a text file (as an external function);
- write the graph from a text file (as an external function);
- create a random graph with specified number of vertices and of edges (as an external function);
- get the number of vertices of the graph;
- parse (iterate) the set of vertices of the graph;
- given two vertices, find out whether there is an edge from the first one to the second one;
- get the in degree and the out degree of a specified vertex;
- parse the set of outbound edges of a specified vertex;
- parse the set of inbound edges of a specified vertex;
- display the vertices and the edges of the graph;
- retrieve or modify the information (the cost) attached to a specified edge;
- add and remove an edge;
- add and remove a vertex;
- make an exact copy of a graph, so that the original can be then modified independently of its copy; 
- display the list of isolated vertices;
- find the connected components of an undirected graph using a breadth-first traversal of the graph;
- find a lowest cost walk between the given vertices, using a "backwards" Dijkstra algorithm (Dijkstra algorithm that searches backwards, from the ending vertex);
- verify if the corresponding graph is a DAG and performs a topological sorting of the activities using the algorithm based on depth-first traversal (Tarjan's algorithm); if it is a DAG, finds a highest cost path between two given vertices, in O(m+n);
- given a digraph with costs and two vertices, find a minimum cost path between them (negative cost cycles may exist in the graph);

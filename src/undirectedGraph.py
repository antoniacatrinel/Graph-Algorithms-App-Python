from exceptions import *
import copy


class UndirectedGraph:
    def __init__(self, number_of_vertices):
        self.__no_of_vertices = number_of_vertices
        self.__neighbors = {}
        self.__costs = {}

        for vertex in range(self.__no_of_vertices):
            self.__neighbors[vertex] = []

    @property
    def get_no_of_vertices(self):
        """
        :return: number of vertices of the graph
        """
        return self.__no_of_vertices

    @property
    def get_no_of_edges(self):
        """
        :return: number of edges of the graph
        """
        return len(self.__costs.keys())

    @property
    def get_neighbors(self):
        """
        :return: neighbours of the graph
        """
        return self.__neighbors

    @property
    def get_costs(self):
        """
        :return: costs of the graph
        """
        return self.__costs

    def get_cost_of_edge(self, start_vertex, end_vertex):
        """
        :return: cost of given edge if it exists
        :raises GraphException: nonexistent vertices or edge
        """
        if start_vertex not in self.__neighbors or end_vertex not in self.__neighbors:
            raise GraphException("Nonexistent vertex!\n")

        if self.is_edge(start_vertex, end_vertex) is False:
            raise GraphException("Nonexistent edge!\n")

        if (start_vertex, end_vertex) in self.__costs.keys():
            return self.__costs[(start_vertex, end_vertex)]
        else:
            return self.__costs[(end_vertex, start_vertex)]

    def get_isolated_vertices(self):
        """
        :return: list of isolated vertices
        """
        isolated = []
        for vertex in self.__neighbors.keys():
            if len(self.__neighbors[vertex]) == 0:
                isolated.append(vertex)

        return isolated[:]

    def get_degree_of_vertex(self, vertex):
        """
        Gets the in degree of given vertex
        :return: integer representing the in degree
        :raises GraphException if vertex is invalid
        """
        try:
            return len(self.__neighbors[vertex])
        except KeyError:
            raise GraphException("Nonexistent vertex!\n")

    def parse_all_vertices(self):
        """
        :return: a list containing all keys = vertices
        """
        return list(self.__neighbors.keys())

    def parse_all_edges(self):
        """
        :return: a list containing all keys = edges
        """
        return list(self.__costs.keys())

    def parse_neighbors(self, vertex):
        """
        :param vertex: vertex whose neighbors are searched
        :return: a list of all neighbors of given vertex
        :raises GraphException: nonexistent vertex
        """
        try:
            return list(self.__neighbors[vertex])
        except KeyError:
            raise GraphException("Nonexistent vertex!\n")

    def is_edge(self, start_vertex, end_vertex):
        """
        Checks if there is an edge between the 2 given vertices
        :return: true if there is an edge from start_vertex to end_vertex, false otherwise
        :raises GraphException: nonexistent edge
        """
        try:
            return end_vertex in self.__neighbors[start_vertex] and start_vertex in self.__neighbors[end_vertex]
        except KeyError:
            raise GraphException("There isn't an edge between these 2 vertices in the graph!\n")

    def add_edge(self, start_vertex, end_vertex, cost):
        """
        Adds a new edge (start_vertex, end_vertex) to the graph
        :param start_vertex: start of edge
        :param end_vertex: end of edge
        :param cost: cost of edge
        :raises GraphException: if edge already exists in the graph or vertices are invalid
        """
        if start_vertex not in self.__neighbors.keys() or end_vertex not in self.__neighbors.keys():
            raise GraphException("Nonexistent vertex!\n")

        if int(start_vertex) == int(end_vertex):
            raise GraphException("Cannot have loops!\n")

        if self.is_edge(start_vertex, end_vertex):
            raise GraphException("Edge already exists in the graph!\n")

        self.__neighbors[start_vertex].append(end_vertex)
        self.__neighbors[end_vertex].append(start_vertex)
        self.__costs[(start_vertex, end_vertex)] = cost

    def remove_edge(self, start_vertex, end_vertex):
        """
        Removes an edge (start_vertex, end_vertex) from the graph
        :param start_vertex: start of edge
        :param end_vertex: end of edge
        :raises GraphException if edge doesn't exist in the graph or vertices are invalid
        """
        if start_vertex not in self.__neighbors.keys() or end_vertex not in self.__neighbors.keys():
            raise GraphException("Nonexistent vertex!\n")

        if not self.is_edge(start_vertex, end_vertex):
            raise GraphException("Edge doesn't exist!\n")

        self.__neighbors[start_vertex].remove(end_vertex)
        self.__neighbors[end_vertex].remove(start_vertex)

        if (start_vertex, end_vertex) in self.__costs.keys():
            del self.__costs[(start_vertex, end_vertex)]
        else:
            del self.__costs[(end_vertex, start_vertex)]

    def add_vertex(self, new_vertex):
        """
        Adds a new vertex to the graph
        :param new_vertex: vertex to be added
        :raises GraphException if vertex already exists in the graph
        """
        err = ""
        if new_vertex in self.__neighbors.keys():
            err += "Vertex already exists in the graph!\n"

        if len(err) > 0:
            raise GraphException(err)

        self.__neighbors[new_vertex] = []
        self.__no_of_vertices += 1

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph
        :param vertex: vertex to be removed
        :raises GraphException if vertex doesn't exist in the graph
        """
        if vertex not in self.__neighbors.keys():
            raise GraphException("Nonexistent vertex!\n")

        for start_vertex in self.__neighbors[vertex]:
            self.__neighbors[start_vertex].remove(vertex)
            if (start_vertex, vertex) in self.__costs.keys():
                del self.__costs[(start_vertex, vertex)]
            else:
                del self.__costs[(vertex, start_vertex)]

        # remove vertex
        del self.__neighbors[vertex]
        self.__no_of_vertices -= 1

    def copy_graph(self):
        """
        :return: deepcopy copy of current graph
        """
        graph_copy = UndirectedGraph(self.__no_of_vertices)
        graph_copy.__no_of_vertices = self.__no_of_vertices
        graph_copy.__neighbors = copy.deepcopy(self.__neighbors)
        graph_copy.__costs = copy.deepcopy(self.__costs)

        return graph_copy

    def update_cost(self, start_vertex, end_vertex, new_cost):
        """
        Changes the cost of an edge (start_vertex, end_vertex) with given value
        :raises GraphException if edge doesn't exit in the graph
        """
        if start_vertex not in self.__neighbors or end_vertex not in self.__neighbors:
            raise GraphException("Nonexistent vertex!\n")

        if self.is_edge(start_vertex, end_vertex) is False:
            raise GraphException("Nonexistent edge!\n")

        if (start_vertex, end_vertex) in self.__costs.keys():
            self.__costs[(start_vertex, end_vertex)] = new_cost
        else:
            self.__costs[(end_vertex, start_vertex)] = new_cost

    def iterable_edges(self):
        """
        :return: returns the edges of a graph in iterable form
        """
        edges = []
        for edge in self.__costs:
            edges.append(edge)

        return edges[:]

    def iterable_costs(self):
        """
        :return: returns the costs of a graph in iterable form
        """
        costs = []
        for cost in self.__costs:
            costs.append(self.__costs[cost])

        return costs[:]

    def breadth_first_search(self, source_vertex, is_visited):
        """
        Method that performs a breadth-first traversal of graph
        :param is_visited: boolean list which is True for each vertex that has been visited and False otherwise
        :param source_vertex: start vertex of graph traversal
        :return: list containing the connected component that starts from given vertex
        """
        # list containing vertices of the found connected component
        connected_component = []

        # list of all traversed vertices from the graph
        queue = []

        # mark source vertex as visited and add it to connected component
        is_visited[source_vertex] = True
        queue.append(source_vertex)

        # parse the queue until it's empty
        while len(queue) > 0:
            # pop first element from the queue
            vertex = queue.pop(0)
            # add first element to component
            connected_component.append(vertex)
            # parse all neighbors of current vertex
            for neighbor in self.__neighbors[vertex]:
                if is_visited[neighbor] is False:
                    queue.append(neighbor)     # append neighbor to parsed vertices queue
                    is_visited[neighbor] = True        # mark neighbor as visited

        return connected_component[:]

    def get_all_connected_components(self):
        """
        Method that finds all the connected components in the given undirected graph
        :return: a list of all the connected components
        """
        # list that holds all connected components of graph
        connected_components = []
        # list that holds all visited vertices
        is_visited = [False] * (self.__no_of_vertices + 1)

        for vertex in self.parse_all_vertices():
            if is_visited[vertex] is False:
                # call BFS algorithm for each vertex of graph
                new_component = self.breadth_first_search(vertex, is_visited)
                connected_components.append(new_component)

        return connected_components

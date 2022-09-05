from queue import PriorityQueue
from exceptions import *
from math import inf
import copy


class DirectedGraph:
    def __init__(self, number_of_vertices):
        self.__no_of_vertices = number_of_vertices
        self.__outbound_neighbors = {}
        self.__inbound_neighbors = {}
        self.__costs = {}

        for vertex in range(self.__no_of_vertices):
            self.__outbound_neighbors[vertex] = []
            self.__inbound_neighbors[vertex] = []

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
    def get_out_neighbors(self):
        """
        :return: outbound neighbours of the graph
        """
        return self.__outbound_neighbors

    @property
    def get_in_neighbors(self):
        """
        :return: inbound neighbours of the graph
        """
        return self.__inbound_neighbors

    @property
    def get_costs(self):
        """
        :return: costs of the graph
        """
        return self.__costs

    def get_cost_of_edge(self, start_vertex, end_vertex):
        """
        :return: cost of given edge if it exists
        """
        if self.is_edge(start_vertex, end_vertex):
            return self.__costs[(start_vertex, end_vertex)]

    def get_isolated_vertices(self):
        """
        :return: list of isolated vertices
        """
        isolated = []
        for vertex in self.parse_dictionary_keys():
            if len(self.__inbound_neighbors[vertex]) == 0 and len(self.__outbound_neighbors[vertex]) == 0:
                isolated.append(vertex)

        return isolated[:]

    def get_in_degree(self, vertex):
        """
        Gets the in degree of given vertex
        :return: integer representing the in degree
        :raises GraphException if vertex is invalid
        """
        try:
            return len(self.__inbound_neighbors[vertex])
        except KeyError:
            raise GraphException("Nonexistent vertex!\n")

    def get_out_degree(self, vertex):
        """
        Gets the out degree of given vertex
        :return: integer representing the out degree
        :raises GraphException if vertex is invalid
        """
        try:
            return len(self.__outbound_neighbors[vertex])
        except KeyError:
            raise GraphException("Nonexistent vertex!\n")

    def parse_dictionary_keys(self):
        """
        :return: a list containing all keys = vertices
        """
        return list(self.__outbound_neighbors.keys())

    def parse_outbound_neighbors(self, vertex):
        """
        :param vertex: vertex whose neighbors are searched
        :return: a list of all outbound neighbors of given vertex
        :raises GraphException if vertex is invalid
        """
        try:
            return list(self.__outbound_neighbors[vertex])
        except KeyError:
            raise GraphException("Nonexistent vertex!\n")

    def parse_inbound_neighbors(self, vertex):
        """
        :param vertex: vertex whose neighbors are searched
        :return: a list of all inbound neighbors of given vertex
        :raises GraphException if vertex is invalid
        """
        try:
            return list(self.__inbound_neighbors[vertex])
        except KeyError:
            raise GraphException("Nonexistent vertex!\n")

    def is_edge(self, start_vertex, end_vertex):
        """
        Checks if there is an edge between the 2 given vertices
        :return: true if there is an edge from start_vertex to end_vertex, false otherwise
        :raises GraphException: nonexistent edge
        """
        try:
            return end_vertex in self.__outbound_neighbors[start_vertex]
        except KeyError:
            raise GraphException("There isn't an edge between these 2 vertices in the graph!\n")

    def add_edge(self, start_vertex, end_vertex, cost):
        """
        Adds a new edge (start_vertex, end_vertex) to the graph
        :param start_vertex: start of edge
        :param end_vertex: end of edge
        :param cost: cost of edge
        :raises GraphException if edge already exists in the graph or vertices are invalid
        """
        err = ""
        if self.is_edge(start_vertex, end_vertex):
            err += "Edge already exists in the graph!\n"

        if len(err) > 0:
            raise GraphException(err)

        self.__outbound_neighbors[start_vertex].append(end_vertex)
        self.__inbound_neighbors[end_vertex].append(start_vertex)
        self.__costs[(start_vertex, end_vertex)] = cost

    def remove_edge(self, start_vertex, end_vertex):
        """
        Removes an edge (start_vertex, end_vertex) from the graph
        :param start_vertex: start of edge
        :param end_vertex: end of edge
        :raises GraphException if edge doesn't exist in the graph or vertices are invalid
        """
        if not self.is_edge(start_vertex, end_vertex):
            raise GraphException("Edge doesn't exist!\n")

        self.__outbound_neighbors[start_vertex].remove(end_vertex)
        self.__inbound_neighbors[end_vertex].remove(start_vertex)
        del self.__costs[(start_vertex, end_vertex)]

    def add_vertex(self, new_vertex):
        """
        Adds a new vertex to the graph
        :param new_vertex: vertex to be added
        :raises GraphException if vertex already exists in the graph
        """
        err = ""
        if new_vertex in self.parse_dictionary_keys():
            err += "Vertex already exists in the graph!\n"

        if len(err) > 0:
            raise GraphException(err)

        self.__outbound_neighbors[new_vertex] = []
        self.__inbound_neighbors[new_vertex] = []
        self.__no_of_vertices += 1

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph
        :param vertex: vertex to be removed
        :raises GraphException if vertex doesn't exist in the graph
        """
        if vertex not in self.parse_dictionary_keys():
            raise GraphException("Nonexistent vertex!\n")

        # remove all edges that start from given vertex -> outbound neighbors
        for end_vertex in self.__outbound_neighbors[vertex]:
            self.__inbound_neighbors[end_vertex].remove(vertex)
            del self.__costs[(vertex, end_vertex)]

        # remove all edges that end in given vertex -> inbound neighbors
        for start_vertex in self.__inbound_neighbors[vertex]:
            self.__outbound_neighbors[start_vertex].remove(vertex)
            del self.__costs[(start_vertex, vertex)]

        # remove vertex
        del self.__outbound_neighbors[vertex]
        del self.__inbound_neighbors[vertex]
        self.__no_of_vertices -= 1

    def copy_graph(self):
        """
        :return: deepcopy copy of current graph
        """
        graph_copy = DirectedGraph(self.__no_of_vertices)
        graph_copy.__no_of_vertices = self.__no_of_vertices
        graph_copy.__outbound_neighbors = copy.deepcopy(self.__outbound_neighbors)
        graph_copy.__inbound_neighbors = copy.deepcopy(self.__inbound_neighbors)
        graph_copy.__costs = copy.deepcopy(self.__costs)

        return graph_copy

    def update_cost(self, start_vertex, end_vertex, new_cost):
        """
        Changes the cost of an edge (start_vertex, end_vertex) with given value
        :raises GraphException if edge doesn't exit in the graph
        """
        if (start_vertex, end_vertex) in self.__costs:
            self.__costs[(start_vertex, end_vertex)] = new_cost
        else:
            raise GraphException("Nonexistent edge!")

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

    def get_lowest_cost_path(self, start_vertex, end_vertex):
        """
        Finds the lowest cost path between 2 vertices
        :param start_vertex: starting vertex of path
        :param end_vertex: ending vertex of path
        """
        # call the function to get the distance and the next dictionary
        dist, next = self.backwards_Dijkstra(start_vertex, end_vertex)
        # we dont have a walk
        if dist[start_vertex] == 100000000001:
            raise GraphException("No walk!")

        # form the path from next dictionary
        path = []
        v = start_vertex
        while v != end_vertex:
            path.append(v)
            v = next[v]

        path.append(end_vertex)
        return path, dist[start_vertex]

    def backwards_Dijkstra(self, start_vertex, end_vertex=None):
        """
        Finds a lowest cost walk between the given vertices, using a "backwards" Dijkstra algorithm
        :param start_vertex: starting vertex of path
        :param end_vertex: ending vertex of path
        """
        q = PriorityQueue()
        # dictionary that holds for each vertex the cost of the minimum cost walk
        dist = {}
        for i in range(self.__no_of_vertices):
            dist[i] = 100000000001
        # dictionary that holds for each vertex its successor on the path
        next = {}
        # initialize the lowest cost walk to end_vertex with 0
        dist[end_vertex] = 0
        # add the tuple(stance, vertex) to the priority queue
        q.put((dist[end_vertex], end_vertex))

        visited = set()
        visited.add(end_vertex)
        while not q.empty():
            # get the last item from the queue
            distance, vertex = q.get()

            # go through the inbound neighbor of the vertex
            # check if the distance is minimum
            # if it is, add it to the path and update the distance to the vertex neighbor from the end_vertex
            for neighbor in self.__inbound_neighbors[vertex]:
                if neighbor not in visited or dist[neighbor] > dist[vertex] + self.__costs[(neighbor, vertex)]:
                    dist[neighbor] = dist[vertex] + self.__costs[(neighbor, vertex)]
                    visited.add(vertex)
                    q.put((dist[neighbor], neighbor))
                    next[neighbor] = vertex
        return dist, next

    def topological_sort_DFS(self, vertex, sorted, fully_processed, in_process):
        """
        Performs a topological sorting of the activities using the algorithm based on depth-first traversal (Tarjan's algorithm)
        :param vertex: starting vertex
        :param sorted: list of sorted vertices
        :param fully_processed: list of fully processed vertices
        :param in_process: list of vertices which are currently in process
        """
        in_process.add(vertex)
        for inbound_neighbour in self.parse_inbound_neighbors(vertex):
            if inbound_neighbour in in_process:
                return False
            else:
                if inbound_neighbour not in fully_processed:
                    ok = self.topological_sort_DFS(inbound_neighbour, sorted, fully_processed, in_process)
                    if not ok:
                        print(sorted)
                        return False

        in_process.remove(vertex)
        sorted.append(vertex)
        fully_processed.add(vertex)
        return True

    def DAG(self):
        """
        Verifies if the corresponding graph is a DAG (Directed Acyclic Graph)
        """
        sorted = []
        fully_processed = set()
        in_process = set()
        for vertex in self.parse_dictionary_keys():
            if vertex not in fully_processed:
                ok = self.topological_sort_DFS(vertex, sorted, fully_processed, in_process)
                if not ok:
                    return []
        return sorted[:]

    def highest_cost_path(self, sorted, start_vertex, end_vertex):
        """
        Finds a highest cost path between two given vertices
        :param sorted: list of sorted vertices
        :param start_vertex: starting vertex
        :param end_vertex: ending vertex
        :return:
        """
        distances = [-inf] * len(sorted)
        prev = [-1] * len(sorted)
        distances[start_vertex] = 0
        for vertex in sorted:
            if vertex == end_vertex:
                break
            for outbound_neighbour in self.parse_outbound_neighbors(vertex):
                if distances[outbound_neighbour] < distances[vertex] + self.get_cost_of_edge(vertex, outbound_neighbour):
                    distances[outbound_neighbour] = distances[vertex] + self.get_cost_of_edge(vertex, outbound_neighbour)
                    prev[outbound_neighbour] = vertex
        return distances[end_vertex], prev[:]

    def bellman_ford(self, start_vertex, max_length):
        """
        Bellman Ford algorithm used to find the shortest path from the source vertex to every vertex in a weighted graph
        :param start_vertex: starting vertex
        :param max_length: maximum length of the path
        :return: all the possible distances with length < max_length
        """
        # initial_dict = {start_vertex: 0}
        initial_dict = dict.fromkeys(range(start_vertex + 1), 0)
        distances = [initial_dict]
        for k in range(1, max_length + 1):
            previous_dict = distances[k - 1]
            current_dict = {}
            for vertex1 in previous_dict:
                for vertex2 in self.parse_outbound_neighbors(vertex1):
                    if vertex2 not in current_dict or current_dict[vertex2] > previous_dict[vertex1] + self.get_cost_of_edge(vertex1, vertex2):
                        current_dict[vertex2] = previous_dict[vertex1] + self.get_cost_of_edge(vertex1, vertex2)
            distances.append(current_dict)
        return distances

    def min_cost_path_neg_cycle(self, distances, start_vertex, end_vertex, length):
        """
        Finds the minimum cost path between 2 vertices with given length
        """
        walk = []
        current_vertex = end_vertex
        current_length = length
        while current_length > 0:
            walk.insert(0, current_vertex)
            for previous_vertex in self.parse_inbound_neighbors(current_vertex):
                if previous_vertex in distances[current_length - 1] and distances[current_length - 1][previous_vertex] + \
                        self.get_cost_of_edge(previous_vertex, current_vertex) == distances[current_length][current_vertex]:
                    current_vertex = previous_vertex
                    break
            current_length -= 1
        walk.insert(0, start_vertex)
        return walk

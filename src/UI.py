from directedGraph import *
from random import randint
from math import inf


class UI:
    def __init__(self, file_name):
        self.__graph = DirectedGraph(0)
        self.__copy = DirectedGraph(0)
        self.__file = file_name
        self.__dict_of_options = {
            "1": self.load_graph_from_file,
            "2": self.generate_random_graph,
            "3": self.print_number_of_vertices,
            "4": self.print_vertices,
            "5": self.is_edge_between,
            "6": self.get_vertex_degrees,
            "7": self.parse_outbound_neighbors,
            "8": self.parse_inbound_neighbors,
            "9": self.update_cost_of_edge,
            "10": self.add_new_vertex,
            "11": self.add_new_edge,
            "12": self.remove_vertex,
            "13": self.remove_edge,
            "14": self.print_graph,
            "15": self.copy_current_graph,
            "16": self.print_graph_copy,
            "17": self.print_isolated_vertices,
            "18": self.write_graph_to_file_ui,
            "19": self.parse_all_neighbors,
            "20": self.lowest_cost_walk,
            "21": self.is_graph_DAG,
            "22": self.get_lowest_cost_path_neg_cycles
        }

    @staticmethod
    def print_menu():
        print("-" * 75)
        print(" Menu:")
        print("    >> Press 1 to load the graph from file")
        print("    >> Press 2 to generate a random graph and write it to a file")
        print("    >> Press 3 to display the number of vertices")
        print("    >> Press 4 to get all vertices")
        print("    >> Press 5 to check if there is an edge from vertex v1 to vertex v2")
        print("    >> Press 6 to display the in and out degree of a vertex")
        print("    >> Press 7 to parse the outbound neighbors of a vertex")
        print("    >> Press 8 to parse the inbound neighbors of a vertex")
        print("    >> Press 9 to modify the cost of an edge")
        print("    >> Press 10 to add a vertex to the graph")
        print("    >> Press 11 to add an edge to the graph")
        print("    >> Press 12 to remove a vertex from the graph")
        print("    >> Press 13 to remove an edge from the graph")
        print("    >> Press 14 to display the graph's vertices and edges")
        print("    >> Press 15 to make a copy of the current graph")
        print("    >> Press 16 to display the copy of the graph, with its vertices and edges")
        print("    >> Press 17 to display isolated vertices")
        print("    >> Press 18 to write the graph to a new file")
        print("    >> Press 19 to parse the neighbors of a vertex")
        print("    >> Press 20 to find a lowest cost walk between the given vertices, using a backwards Dijkstra algorithm")
        print("    >> Press 21 to verify if the corresponding graph is a DAG and perform a topological sorting of the activities"
              " using the algorithm based on depth-first traversal (Tarjan's algorithm). If it is a DAG, finds a highest cost path between two given vertices, in O(m+n).")
        print("    >> Press 22 to find a minimum cost path between 2 given vertices (negative cost cycles may exist in the graph)")
        print("    >> Press 0 to exit")
        print("-" * 75)

    def load_graph_from_file(self):
        try:
            f = open(self.__file, "rt")
            first = f.readline()
            first = first.strip()
            first = first.split(sep=" ", maxsplit=1)
            number_of_vertices, number_of_edges = int(first[0]), int(first[1])
            self.__graph = DirectedGraph(number_of_vertices)
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    line = line.split(sep=" ", maxsplit=2)
                    start_vertex, end_vertex, cost = int(line[0]), int(line[1]), int(line[2])
                    self.__graph.add_edge(start_vertex, end_vertex, cost)

            f.close()
            print("Graph loaded successfully!\n")
        except IOError:
            raise GraphException("Error reading input file!\n")

    @staticmethod
    def write_graph_to_file(graph):
        file = input("Input the name of the file where you want to save the graph > ")
        f = open(file, "wt")
        first = str(graph.get_no_of_vertices) + " " + str(graph.get_no_of_edges) + "\n"
        f.write(first)

        if int(graph.get_no_of_vertices) == 0 and int(graph.get_no_of_edges) == 0:
            raise GraphException("Nothing can be written to the file!\n")

        for edge in graph.get_costs.keys():
            line = str(edge[0]) + " " + str(edge[1]) + " " + str(graph.get_costs[edge]) + "\n"
            f.write(line)

        for vertex in graph.parse_dictionary_keys():
            if len(graph.get_in_neighbors[vertex]) == 0 and len(graph.get_out_neighbors[vertex]) == 0:
                line = str(vertex) + "\n"
                f.write(line)

        f.close()
        print("Graph written to file successfully!\n")

    def write_graph_to_file_ui(self):
        self.write_graph_to_file(self.__graph)

    def print_number_of_vertices(self):
        print("Number of vertices is " + str(self.__graph.get_no_of_vertices))

    def is_edge_between(self):
        start_vertex = input("Input start vertex: ")
        end_vertex = input("Input end vertex: ")
        start_vertex, end_vertex = self.validator_edge(start_vertex, end_vertex)
        if self.__graph.is_edge(start_vertex, end_vertex) is True:
            print("There is an edge between the given vertices!")
        else:
            print("There isn't an edge between the given vertices!")

    def get_vertex_degrees(self):
        vertex = input("Input a vertex: ")
        vertex = self.validator_vertex(vertex)
        print("The out degree is: " + str(self.__graph.get_out_degree(vertex)))
        print("The in degree is: " + str(self.__graph.get_in_degree(vertex)))

    def add_new_vertex(self):
        vertex = input("Input new vertex: ")
        vertex = self.validator_vertex(vertex)
        self.__graph.add_vertex(vertex)
        print("Vertex added successfully!\n")

    def remove_vertex(self):
        vertex = input("Input vertex to be removed: ")
        vertex = self.validator_vertex(vertex)
        self.__graph.remove_vertex(vertex)
        print("Vertex removed successfully!\n")

    def add_new_edge(self):
        start_vertex = input("Input start vertex: ")
        end_vertex = input("Input end vertex: ")
        cost = input("Input edge's cost: ")
        start_vertex, end_vertex = self.validator_edge(start_vertex, end_vertex)
        cost = self.validator_cost(cost)
        self.__graph.add_edge(start_vertex, end_vertex, cost)
        print("Edge added successfully!\n")

    def remove_edge(self):
        start_vertex = input("Input start vertex: ")
        end_vertex = input("Input end vertex: ")
        start_vertex, end_vertex = self.validator_edge(start_vertex, end_vertex)
        self.__graph.remove_edge(start_vertex, end_vertex)
        print("Edge removed successfully!\n")

    def copy_current_graph(self):
        self.__copy = self.__graph.copy_graph()
        print("Graph copied successfully!\n")

    def update_cost_of_edge(self):
        start_vertex = input("Input start vertex: ")
        end_vertex = input("Input end vertex: ")
        cost = input("Input the new cost of the edge: ")
        start_vertex, end_vertex = self.validator_edge(start_vertex, end_vertex)
        cost = self.validator_cost(cost)
        self.__graph.update_cost(start_vertex, end_vertex, cost)
        print("Cost updated successfully!\n")

    def print_isolated_vertices(self):
        if len(self.__graph.get_isolated_vertices()) == 0:
            print("There are no isolated vertices!\n")
        else:
            print("Isolated vertices: ")
            for vertex in self.__graph.get_isolated_vertices():
                print(str(vertex))

    def print_graph(self):
        ok = 1
        if len(self.__graph.parse_dictionary_keys()) == 0:
            print("There are no vertices in the graph!\n")
            ok = 0
        if ok:
            print("Vertices of the graph are: ")
            for vertex in self.__graph.parse_dictionary_keys():
                print(str(vertex))

            if len(self.__graph.iterable_edges()) == 0:
                print("There are no edges in the graph!\n")
            else:
                print("Edges and costs of the graph are: ")
                for edge in self.__graph.iterable_edges():
                    print(str(edge) + ", " + str(self.__graph.get_costs[edge]))

    def print_graph_copy(self):
        ok = 1
        if len(self.__copy.parse_dictionary_keys()) == 0:
            print("There are no vertices in the copied graph!\n")
            ok = 0
        if ok:
            print("Vertices of the copied graph are: ")
            for vertex in self.__copy.parse_dictionary_keys():
                print(str(vertex))

            if len(self.__copy.iterable_edges()) == 0:
                print("There are no edges in the copied graph!\n")
            else:
                print("Edges and costs of the copied graph are: ")
                for edge in self.__copy.iterable_edges():
                    print(str(edge) + ", " + str(self.__copy.get_costs[edge]))

    def print_vertices(self):
        if len(self.__graph.parse_dictionary_keys()) == 0:
            print("There are no vertices in the graph!\n")
        else:
            print("Vertices of the graph are: ")
            for vertex in self.__graph.parse_dictionary_keys():
                print(str(vertex))

    def parse_outbound_neighbors(self):
        vertex = int(input("Input vertex whose outbound neighbors you want to parse: "))
        out_neighbors = self.__graph.parse_outbound_neighbors(vertex)
        if len(out_neighbors) == 0:
            print("Given vertex doesn't have outbound neighbors!\n")
        else:
            print("Outbound neighbors of given vertex are: ")
            for vertex in out_neighbors:
                print(str(vertex))

    def parse_inbound_neighbors(self):
        vertex = int(input("Input vertex whose inbound neighbors you want to parse: "))
        in_neighbors = self.__graph.parse_inbound_neighbors(vertex)
        if len(in_neighbors) == 0:
            print("Given vertex doesn't have inbound neighbors!\n")
        else:
            print("Inbound neighbors of given vertex are: ")
            for vertex in in_neighbors:
                print(str(vertex))

    def parse_all_neighbors(self):
        vertex = int(input("Input vertex whose outbound neighbors you want to parse: "))
        out_neighbors = self.__graph.parse_outbound_neighbors(vertex)
        if len(out_neighbors) == 0:
            print("Given vertex doesn't have outbound neighbors!\n")
        else:
            print("Outbound neighbors of given vertex are: ")
            for vertex in out_neighbors:
                print(str(vertex))
        in_neighbors = self.__graph.parse_inbound_neighbors(vertex)
        if len(in_neighbors) == 0:
            print("Given vertex doesn't have inbound neighbors!\n")
        else:
            print("Inbound neighbors of given vertex are: ")
            for vertex in in_neighbors:
                print(str(vertex))

    def lowest_cost_walk(self):
        start_vertex = input("Input start vertex: ")
        end_vertex = input("Input end vertex: ")
        start_vertex = self.validator_vertex(start_vertex)
        end_vertex = self.validator_vertex(end_vertex)
        if start_vertex not in self.__graph.parse_dictionary_keys():
            raise GraphException("Start vertex does not exist in the graph!")

        if end_vertex not in self.__graph.parse_dictionary_keys():
            raise GraphException("End vertex does not exist in the graph!")

        path, distance = self.__graph.get_lowest_cost_path(start_vertex, end_vertex)
        print("Cost of the lowest cost path is: " + str(distance))
        print("The lowest cost path between the given vertices is:")
        print(path)

    def is_graph_DAG(self):
        dag_sorted = self.__graph.DAG()
        if dag_sorted:
            print("Given graph is DAG!")
            print("Topological sorting with DFS:")
            print(dag_sorted)
            self.get_highest_cost_path(dag_sorted)
        else:
            print("Given graph is not DAG!")

    def get_highest_cost_path(self, sorted_dag):
        print("Input start vertex of highest cost path: ")
        start_vertex = int(input())
        print("Input end vertex of highest cost path: ")
        end_vertex = int(input())
        cost, prev = self.__graph.highest_cost_path(sorted_dag, start_vertex, end_vertex)
        if cost == -inf:
            print("No path!")
            return

        # Construct path
        path = [end_vertex]
        while start_vertex != end_vertex:
            end_vertex = prev[end_vertex]
            path.append(end_vertex)

        print("Cost of path is:")
        print(cost)

        print("Path is: ")
        path.reverse()
        print(path)

    def get_lowest_cost_path_neg_cycles(self):
        start_vertex = int(input("Vertex 1: "))
        end_vertex = int(input("Vertex 2: "))
        max_length = 2 * self.__graph.get_no_of_vertices
        distances = self.__graph.bellman_ford(start_vertex, max_length)

        for vertex1 in self.__graph.parse_dictionary_keys():
            for vertex2 in self.__graph.parse_outbound_neighbors(vertex1):
                if vertex2 in distances[vertex1].keys() and distances[vertex1][vertex1] + self.__graph.get_cost_of_edge(vertex1, vertex2) < distances[vertex2][vertex2]:
                    print("Graph has negative cycles!")
                    return

        tuplee = (999999999, 999999999)
        for vertex1 in range(max_length + 1):
            if end_vertex in distances[vertex1]:
                if tuplee[1] > distances[vertex1][end_vertex]:
                    tuplee = (self.__graph.min_cost_path_neg_cycle(distances, start_vertex, end_vertex, vertex1), distances[vertex1][end_vertex])
        print(tuplee[0], " with cost:", tuplee[1])

    @staticmethod
    def generateGraph(no_of_vertices, no_of_edges):
        graph = DirectedGraph(no_of_vertices)
        index = 0
        while index < no_of_edges:
            start_vertex = randint(0, no_of_vertices - 1)
            end_vertex = randint(0, no_of_vertices - 1)
            cost = randint(0, 200)
            try:
                graph.add_edge(start_vertex, end_vertex, cost)
                index += 1
            except GraphException:
                pass
        return graph

    def generate_random_graph(self):
        no_of_vertices = input("Input the number of vertices: ")
        no_of_edges = input("Input the number of edges: ")
        no_of_vertices = self.validator_no_vertices(no_of_vertices)
        no_of_edges = self.validator_no_edges(no_of_edges)
        if no_of_edges > no_of_vertices * no_of_vertices:
            raise GraphException("Too many edges!\n")
        self.__graph = self.generateGraph(no_of_vertices, no_of_edges)
        print("Graph generated successfully!\n")
        self.write_graph_to_file(self.__graph)
        print("Graph generated successfully!\n")

    @staticmethod
    def validator_vertex(vertex):
        try:
            vertex = int(vertex)
            return vertex
        except ValueError:
            raise GraphException("Vertex must be a positive integer!\n")

    @staticmethod
    def validator_edge(start_vertex, end_vertex):
        try:
            start_vertex = int(start_vertex)
            end_vertex = int(end_vertex)
            return start_vertex, end_vertex
        except ValueError:
            raise GraphException("Vertices must be positive integers!\n")

    @staticmethod
    def validator_cost(cost):
        try:
            cost = int(cost)
            return cost
        except ValueError:
            raise GraphException("Cost must be a positive integer!\n")

    @staticmethod
    def validator_no_edges(edges):
        try:
            edges = int(edges)
            return edges
        except ValueError:
            raise GraphException("Number of edges must be a positive integer!\n")

    @staticmethod
    def validator_no_vertices(vertices):
        try:
            vertices = int(vertices)
            return vertices
        except ValueError:
            raise GraphException("Number of vertices must be a positive integer!\n")

    def start(self):
        print("Welcome!")
        print("If you want to load the graph from the file, press 1")
        print("If you want to generate a random graph, press 2")
        first_option = input("Input command >>> ")
        if first_option == "1":
            try:
                self.load_graph_from_file()
            except GraphException as err:
                print(err)
        elif first_option == "2":
            try:
                self.generate_random_graph()
            except GraphException as err:
                print(err)
        else:
            print("Invalid command! You can only choose between 1 and 2!\n")
        while True:
            self.print_menu()
            user_command = input("Input command >>> ")
            if user_command == "0":
                return
            elif user_command in self.__dict_of_options:
                try:
                    self.__dict_of_options[user_command]()
                except GraphException as err:
                    print(err)
            else:
                print("Invalid command! Must be an integer between 0 and 22!\n")

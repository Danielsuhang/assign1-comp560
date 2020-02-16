import argparse
import sys
import os.path

import random

from node import Node

class Graph():
    def __init__(self, file_path):
        self.read_inputs(file_path)
    
    def read_inputs(self, file_path):
        f = open(file_path, "r")
        self.colors = set(Graph.read_new_line(f))
        nodes = Graph.read_new_line(f)
        self.nodes = {n: Node(n) for n in nodes}
        nodePairs = Graph.read_new_line(f)
        self.build_nodepairs(nodePairs)

    def build_nodepairs(self, nodePairs):
        for nodePair in nodePairs:
            origin, pair = nodePair.split(" ")

            # Process Nodes
            if (origin not in self.nodes):
                self.nodes[origin] = Node(origin)
                print ("Warning: Pair node " + origin + " not in node graph. Added manually.")
            if (pair not in self.nodes):
                self.nodes[pair] = Node(pair)
                print ("Warning: Pair node " + pair + " not in node graph. Added manually.")

            # Add 2 way connections
            self.nodes[origin].neighbors.append(self.nodes[pair])
            self.nodes[pair].neighbors.append(self.nodes[origin])

    def print_graph(self):
        for name, node in self.nodes.items():
            print(name, node.neighbors, node.color)

    @staticmethod    
    def read_new_line(file):
        all_inputs = []
        while True:
            try: 
                c_input = file.readline().rstrip().lstrip()
                print (c_input)
                if c_input.strip() != '': 
                    all_inputs.append(c_input)
                else:
                    break
            except ValueError:
                print ("Invalid Input")
        return all_inputs 

class MostConstrainedBacktrack():
    def __init__(self, graph):
        self.graph = graph
        self.possible_colors = graph.colors

    def run(self):
        self.backtrack_search()
        print("Found solution in ", self._backtrack_steps, " steps: ", self.verify_graph_colors())
        self.graph.print_graph() 
    
    def backtrack_search(self):
        """ Search all nodes, recursively backtrack through graph adding available colors """
        success = True
        self._backtrack_steps = 0
        # Search all Nodes, process Island Nodes
        for _name, node in self.graph.nodes.items():
            if node.color == "":
                success = self.assign_colors_recursive(node) and success
        #if success is false here, it means that one of the "islands" in the graph could not be resolved
        return g, success
    

    def assign_colors_recursive(self, node):
        """This function will assign a color to the node itself and all nodes that it is a parent of"""
        # Each time this is called, we are searching a node:
        self._backtrack_steps += 1

        # Keep Arc consistency here, only consider other available colors
        available_colors = self.get_available_colors(node)
        
        # If there are no available colors, this solution is drawing dead. No reason to continue considering this solution
        if len(available_colors) == 0:
            return False

        for color in available_colors:
            node.color = color
            success = True

            self.test_most_constrained_sort(node)

            # Traverse most constrainted variable (if tie traverse lexagraphically first neighbors)
            for neighbor in sorted(node.neighbors, key=lambda neighbor_node : (len(self.get_available_colors(neighbor_node)), neighbor_node.name)):
                if neighbor.color == "":
                    success = self.assign_colors_recursive(neighbor) and success
            
            # Success means we found a possible solution with this color assignment on this node
            if success: 
                return True
        
        # Unable to find a solution with available colors for this node, reset node color to unexplored
        node.color = "" 
        return False

    #colors should be a set of all possible colors
    def get_available_colors(self, node):
        return list(self.possible_colors- set([n.color for n in node.neighbors]))

    def verify_graph_colors(self):
        num_searched = 0
        print("\nVerifying solution")
        for _name, node in self.graph.nodes.items():
            num_searched += 1
            for neighbor in node.neighbors:
                if neighbor.color == node.color:
                    return False
        print("SEARCHED: " , num_searched)
        return True
    
    def test_most_constrained_sort(self, node):
        print (node.name + " sorted neighbors: ", end="")
        if (len(node.neighbors) == 0):
            print ("No Neighbors")
        sorted_neighbors = sorted(node.neighbors, key=lambda neighbor_node : (len(self.get_available_colors(neighbor_node)), neighbor_node.name))
        node_constrainted_score = [(len(self.get_available_colors(node)), node.name) for node in sorted_neighbors]
        for node_score in node_constrainted_score:
            print (node_score[0], node_score[1], end = ", ")
        print ("\n")

class LocalSearch():
    MAX_NODE_SEARCH_ATTEMPTS = 1000000
    MAX_new_assignment_attempts = 10000
    def __init__(self, graph):
        self.graph = graph
        self.possible_colors = graph.colors
        self.search_attempts = 0
        self.new_assignment_attempts = 0
    
    """Start with initial assignment of random colors for each node"""
    def preprocess_graph_with_random_colors(self):
        for _name, node in self.graph.nodes.items():
            self.assign_node_random_color(node)
    
    def assign_node_random_color(self, node):
        if node.color != "":
            node.color = self.pick_any_random_color()
            for neighbor in node.neighbors:
                self.assign_node_random_color(neighbor)

    def pick_any_random_color(self):
        return list(self.possible_colors)[random.randint(0, len(self.possible_colors) - 1)]
    
    """
    Run Local Search by randomly assigning colors to all nodes.
    Traverse each node to resolve any invalid color arrangements.
    If a node has no more colors to choose from, restart and try again.
    """
    def run(self):
        success = self.valid_graph()  # Initial success condition
        while (self.continue_search_conditions(success)):
            self.new_assignment_attempts += 1
            self.clear_node_colors()
            self.preprocess_graph_with_random_colors()
            success = self.traverse_graph_change_colors()
        self.get_graph_stats()
    
    def continue_search_conditions(self, success):
        return not success and self.search_attempts < self.MAX_NODE_SEARCH_ATTEMPTS \
            and self.new_assignment_attempts < self.MAX_new_assignment_attempts
    
    """Iterate through all nodes randomly, assign nodes to a possible color"""
    def traverse_graph_change_colors(self):
        for node in self.get_random_node_ordering():
            self.search_attempts += 1
            if not self.valid_node(node):
                self.assign_node_available_random_color(node)
                if node.color == "":
                    """No available color for node, restart configuration 
                    (We can also choose to continue our search with other nodes)"""
                    return False
        return True

    def get_random_node_ordering(self):
        nodes = [node for _name, node in self.graph.nodes.items()]
        random.shuffle(nodes)
        return nodes
    
    def valid_node(self, node):
        if node.color == "":
            return False
        for neighbor in node.neighbors:
            if neighbor.color == node.color:
                return False
        return True

    def assign_node_available_random_color(self, node):
        available_colors = self.available_colors(node)
        if len(available_colors) == 0:
            # No possible color can be assigned
            node.color = ""
            return
        node.color = available_colors[random.randint(0, len(available_colors) - 1)]

    def available_colors(self, node):
        return list(self.possible_colors - set([n.color for n in node.neighbors]))
    
    def valid_graph(self):
        num_searched = 0
        for _name, node in self.graph.nodes.items():
            num_searched += 1
            if not self.valid_node(node):
                return False
        return True
 
    def clear_node_colors(self):
        for _name, node in self.graph.nodes.items():
            node.color = ""
    
    def get_graph_stats(self):
        if self.valid_graph():
            print ("Successfully found solution")
        else:
            print ("Failed to find solution")
            if self.search_attempts > self.MAX_NODE_SEARCH_ATTEMPTS:
                print ("Exhausted search maximum of " + self.MAX_NODE_SEARCH_ATTEMPTS+ ", ending local search")
        self.graph.print_graph()
        print (self.search_attempts)
        print (self.new_assignment_attempts)

if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        raise ValueError("No argument given, pass in input file path")
    if (not os.path.isfile(sys.argv[1])):
        raise ValueError("Invalid path, could not find file in path: " + sys.argv[1])
    g = Graph(sys.argv[1])
    local_search = LocalSearch(g)
    local_search.run()
    # constrained_backtrack_search = MostConstrainedBacktrack(g)
    # constrained_backtrack_search.run()
    

"""
Recurisvely give nodes in the graph colors by making copies of the nodes 
Backtracking Search:

Most Constrained Variable
* Better Variable ordering, choose the variable with the fewest possible values (MRV)
** Start with choosing a random variable

Most Constraining Variable
* Choose the variable that imposes the most constraints on other variables

Best to select Most Constrained Variable First, then use most constraining variable to break ties 


Filtering or Forward Checking:
* Keep track of the possible values for each variable. 
Removes values from Y's domain that are inconsistent with the value chosen for X
Terminate a search path whenver any variable has no legal values

Arc Consistency:
arc X -> Y is consistent iff for every value of X, there is some legal Y.
Need to propagate changes to other nodes

Arc Consistency Alg.
"""

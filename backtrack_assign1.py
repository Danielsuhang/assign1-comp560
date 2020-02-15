from node import Node
import argparse
import sys
import os.path

class Graph():
    def __init__(self, file_path):
        self.readInputs(file_path)
    
    def readInputs(self, file_path):
        f = open(file_path, "r")
        self.colors = set(Graph.readUntilNewLine(f))
        nodes = Graph.readUntilNewLine(f)
        self.nodes = {n: Node(n) for n in nodes}
        nodePairs = Graph.readUntilNewLine(f)
        self.buildNodePairs(nodePairs)

    def buildNodePairs(self, nodePairs):
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

    def printGraph(self):
        for name, node in self.nodes.items():
            print(name, node.neighbors, node.color)

    @staticmethod    
    def readUntilNewLine(file):
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

    def runBacktrack(self):
        self.backtrackSearch()
        print("Found solution in ", self.backtrack_steps, " steps: ", self.verifyGraphColors())
        self.graph.printGraph() 
    
    def backtrackSearch(self):
        """ Search all nodes, recursively backtrack through graph adding available colors """
        success = True
        self.backtrack_steps = 0
        # Search all Nodes, process Island Nodes
        for name, node in self.graph.nodes.items():
            if node.color == "":
                success = self.assignColorsRecursive(node) and success
        #if success is false here, it means that one of the "islands" in the graph could not be resolved
        return g, success
    

    def assignColorsRecursive(self, node):
        """This function will assign a color to the node itself and all nodes that it is a parent of"""
        # Each time this is called, we are searching a node:
        self.backtrack_steps += 1

        # Keep Arc consistency here, only consider other available colors
        available_colors = self.getAvailableColors(node)
        
        # If there are no available colors, this solution is drawing dead. No reason to continue considering this solution
        if len(available_colors) == 0:
            return False

        for color in available_colors:
            node.color = color
            success = True

            ##### TEST IF SORT WORKS ######
            print (node.name + " sorted neighbors: ", end="")
            if (len(node.neighbors) == 0):
                print ("No Neighbors")
            sorted_neighbors = sorted(node.neighbors, key=lambda neighbor_node : (len(self.getAvailableColors(neighbor_node)), neighbor_node.name))
            node_constrainted_score = [(len(self.getAvailableColors(node)), node.name) for node in sorted_neighbors]
            for node_score in node_constrainted_score:
                print (node_score[0], node_score[1], end = ", ")
            print ("\n")
            ##### END TEST ####

            # Traverse most constrainted variable (if tie traverse lexagraphically first neighbors)
            for neighbor in sorted(node.neighbors, key=lambda neighbor_node : (len(self.getAvailableColors(neighbor_node)), neighbor_node.name)):
                if neighbor.color == "":
                    success = self.assignColorsRecursive(neighbor) and success
            
            # Success means we found a possible solution with this color assignment on this node
            if success: 
                return True
        
        # Unable to find a solution with available colors for this node, reset node color to unexplored
        node.color = "" 
        return False

    #colors should be a set of all possible colors
    def getAvailableColors(self, node):
        return list(self.possible_colors- set([n.color for n in node.neighbors]))

    def verifyGraphColors(self):
        numSearched = 0
        print("\nVerifying solution")
        for name, node in self.graph.nodes.items():
            numSearched += 1
            nc = node.color
            for neighbor in node.neighbors:
                if neighbor.color == nc:
                    return False
        print("SEARCHED: " , numSearched)
        return True

if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print ("No argument given, pass in input file path")
        exit()
    if (not os.path.isfile(sys.argv[1])):
        print ("Invalid path, could not find file in path: " + sys.argv[1])
        exit()
    g = Graph(sys.argv[1])
    constrained_backtrack_search = MostConstrainedBacktrack(g)
    constrained_backtrack_search.runBacktrack()
    

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

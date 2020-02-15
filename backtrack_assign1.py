from node import Node
import argparse
import sys

class Graph():
    """Use -d flag to load in default values for Graph"""
    def __init__(self):
        self.readInputs()
    
    def readInputs(self):
        f = open("usdata.txt", "r")
        self.colors = set(readUntilNewLine(f))
        nodes = readUntilNewLine(f)
        self.nodes = {n: Node(n) for n in nodes}
        nodePairs = readUntilNewLine(f)
        self.buildNodePairs(nodePairs)

    def buildNodePairs(self, nodePairs):
        for nodePair in nodePairs:
            origin, pair = nodePair.split(" ")

            # Process Nodes
            origin = origin.rstrip().lstrip()
            pair = pair.rstrip().lstrip()
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

#colors should be a set of all possible colors
def get_available_colors(node, colors):
    return list(colors - set([n.color for n in node.neighbors]))

backtrack_steps = 0

'''
This function will assign a color to the node itself and all nodes that it is a parent of
'''
def assignColorsRecursive(node, colors):
    global backtrack_steps
    # Each time this is called, we are searching a node:
    backtrack_steps += 1

    # Keep Arc consistency here, only consider other available colors
    available_colors = get_available_colors(node, colors)
    
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
        sorted_neighbors = sorted(node.neighbors, key=lambda neighbor_node : (len(get_available_colors(neighbor_node, colors)), neighbor_node.name))
        node_constrainted_score = [(len(get_available_colors(node,colors)), node.name) for node in sorted_neighbors]
        for node_score in node_constrainted_score:
            print (node_score[0], node_score[1], end = ", ")
        print ("\n")
        ##### END TEST ####

        # Traverse most constrainted variable (if tie traverse lexagraphically first neighbors)
        for neighbor in sorted(node.neighbors, key=lambda neighbor_node : (len(get_available_colors(neighbor_node, colors)), neighbor_node.name)):
            if neighbor.color == "":
                success = assignColorsRecursive(neighbor, colors) and success
        
        # Success means we found a possible solution with this color assignment on this node
        if success: 
            return True
    
    # Unable to find a solution with available colors for this node, reset node color to unexplored
    node.color = "" 
    return False

def backtrack_search(g):
    success = True
    # Search all Nodes, process Island Nodes
    for name, node in g.nodes.items():
        if node.color == "":
            success = assignColorsRecursive(node, g.colors) and success
    #if success is false here, it means that one of the "islands" in the graph could not be resolved
    return g, success

    

def verify_graph_colors(g):
    numSearched = 0
    print("\nVerifying solution")
    for name, node in g.nodes.items():
        numSearched += 1
        nc = node.color
        for neighbor in node.neighbors:
            if neighbor.color == nc:
                return False
    print("SEARCHED: " , numSearched)
    return True

if __name__ == "__main__":
    g = Graph()
    g, success = backtrack_search(g)
    print("Found solution in ", backtrack_steps, " steps: ", verify_graph_colors(g))
    g.printGraph()
    

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

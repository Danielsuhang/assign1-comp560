from node import Node
import argparse
import sys

class Graph():
    """Use -d flag to load in default values for Graph"""
    def __init__(self, use_default_nodes):
        if (use_default_nodes):
            self.colors = {'Red', 'Green', 'Blue'}
            self.nodes = {n: Node(n) for n in ['NSW', 'V', 'SA', 'WA', 'NT', 'Q', 'TZ']}
            self.buildNodePairs(['NSW Q', 'NSW V', 'NSW SA', 'V SA', 'Q NT', 'Q SA', 'NT WA', 'NT SA', 'WA SA'])
        else:
            self.readInputs()
        
        self.printGraph()
    
    def readInputs(self):
        self.colors = set(readUntilNewLine())
        nodes = readUntilNewLine()
        self.nodes = {n: Node(n) for n in nodes}
        nodePairs = readUntilNewLine()
        self.buildNodePairs(nodePairs)

    def buildNodePairs(self, nodePairs):
        for nodePair in nodePairs:
             origin, pair = nodePair.split(" ")
             #2 way connections
             self.nodes[origin].neighbors.append(self.nodes[pair])
             self.nodes[pair].neighbors.append(self.nodes[origin])

    def printGraph(self):
        for name, node in self.nodes.items():
            print(name, node.neighbors, node.color)
        

        
def readUntilNewLine():
    all_inputs = []
    while True:
        try: 
            c_input = str(input())
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
    #each time this is called, we are searching a node:
    backtrack_steps += 1

    #Keep Arc consistency here, only consider other available colors
    available_colors = get_available_colors(node, colors)
    
    #if there are no available colors, this solution is drawing dead. No reason to continue considering this solution
    if len(available_colors) == 0:
        return False

    #now for each available color, try using that color for this node
    for color in available_colors:
        node.color = color
        success = True

        #try to recurse on each neighbor with the current node color
        for neighbor in node.neighbors:
            if neighbor.color == "":
                success = assignColorsRecursive(neighbor, colors) and success
        
        #if we successfully recursed on each other node, return true as we found a solution for this node
        if success: 
            return True
    
    #if we made it to here, this means we were unable to find a solution for any of the available colors for this node. Reset the color and report the failure
    node.color = "" 
    return False

def backtrack_search(g):
    success = True
    #this loop is required because it's possible to have nodes that are not connected to any other nodes. One call will be made per "island" in the graph
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
    fp = sys.argv[1]
    g = Graph(False)
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

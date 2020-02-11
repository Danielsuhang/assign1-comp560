from node import Node
import argparse

class Backtrack():
    """Use -d flag to load in default values for Graph"""
    def __init__(self, use_default_nodes):
        if (use_default_nodes):
            self.colors = ['Red', 'Green', 'Blue']
            self.nodes = {n: Node(n) for n in ['NSW', 'V', 'SA', 'WA', 'NT', 'Q', 'TZ']}
            self.buildNodePairs(['NSW Q', 'NSW V', 'NSW SA', 'V SA', 'Q NT', 'Q SA', 'NT WA', 'NT SA', 'WA SA'])
        else:
            self.readInputs()
        
        self.printGraph()
    
    def readInputs(self):
        self.colors = readUntilNewLine()
        nodes = readUntilNewLine()
        self.nodes = {n: Node(n) for n in nodes}
        nodePairs = readUntilNewLine()
        self.buildNodePairs(nodePairs)

    def buildNodePairs(self, nodePairs):
        for nodePair in nodePairs:
             origin, pair = nodePair.split(" ")
             if origin not in self.nodes.keys():
                 print(origin + " is not a valid Node")
                 break 
             self.nodes[origin].neighbors.append(pair)

    def printGraph(self):
        for name, node in self.nodes.items():
            print(name, node.neighbors)
        

        
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true')
    args = parser.parse_args()
    backtrack = Backtrack(args.d)

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

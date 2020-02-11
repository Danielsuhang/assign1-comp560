from node import Node
class Backtrack():
    def __init__(self):
        self.colors = readUntilNewLine()
        nodes = readUntilNewLine()
        self.nodes = {n: Node(n) for n in nodes}
        self.buildNodePairs()
    
    def buildNodePairs(self):
        nodePairs = readUntilNewLine()
        for nodePair in nodePairs:
             pair = nodePair.split(" ")
             self.nodes[pair[0]].neighbors.append(pair[1])

        
def readUntilNewLine():
    all_inputs = []
    while True:
        c_input = input()
        if c_input.strip() != '': 
            all_inputs.append(c_input)
        else:
            break
    return all_inputs 

if __name__ == "__main__":
    backtrack = Backtrack()
    print (backtrack.nodes)


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

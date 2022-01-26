'''
Dijkstra's algorithm
by Carol Browning, January 26, 2020
Updated January 22, 2022
'''
#Code for user Input:
# goal = input("")

# Describe graph with list of vertex labels and adjacency matrix.

V=["A","B","C","D","E"]

'''
Change adjacency matrix to reflect graph given in the assignment.
'''

adjMatrix1 =[[0,3,0,7,0],[3,0,4,2,0],[0,4,0,5,6],[7,2,5,0,4],[0,0,6,4,0]]
# First one is all the values it takes A to get to.
#OG Matrix
adjMatrix = [[0,6,0,2,0], [6,0,1,3,0], [0,1,0,2,2], [2,3,2,0,6], [0,0,2,6,0]]
#adjMatrix = [[0,6,0,2,0], [6,0,1,3,0], [0,1,0,2,2], [0,0,2,6,0], [2,3,2,0,6] ]



# Set infinity to a number that is larger than any path cost.  This
# is the total if you went across every edge twice.
inf = sum([sum(a) for a in adjMatrix])  

# For larger problems change this code to use a priority queue to
# maintain the incomplete list.

# Elements of the vertex class have these attributes:
# label - used for printing the paths,
# path cost - lowest path cost seen so far,
# path parent - parent on path of lowest cost so far,
# index - the index for this vertex in the adjacency matrix.

class Vertex:
    def __init__(self,label,pathCost,pathParent):
        self.label = label 
        self.pathCost = pathCost 
        self.pathParent = pathParent 
        self.index = 0 

# smallest finds vertex with smallest pathCost in given vertex list.
def smallest(vlist): 
    vertexWithSmallestPath = vlist[0]
    for vertex in vlist:
      if vertex.pathCost < vertexWithSmallestPath.pathCost:
        vertexWithSmallestPath = vertex
    return vertexWithSmallestPath
    
def main(input1, input2):
    # Initialize the list of vertex objects.
    vertexlist = [Vertex(vertex,inf,None) for vertex in V]
    for i in range(len(vertexlist)): 
        vertexlist[i].index = i
        if vertexlist[i].label == input1:
            inputIndex = i
    # Our path starts at the first vertex.  Cost to get there is 0.
    
    vertexlist[inputIndex].pathCost = 0
    # Say A is the parent of itself to indicate starting node.
    vertexlist[inputIndex].pathParent = vertexlist[inputIndex]
    # We'll collect the nodes in the path in answer.
    answer = []
    # incompleteList is a list of nodes for which shortest path is not yet
    # determined.
    incompleteList = vertexlist.copy()

    # Dijkstra's algorithm:
    while incompleteList != []:
        # Find the uncompleted vertex with smallest path cost.  
        bestV = smallest(incompleteList)
        # We now know the shortest path to bestV, so add that to our answer.
        answer.append(bestV)
        # If the the smallest vertex equals the input then break the while loop
        if bestV.label == input2:
              break
        # We have finished processing bestV so remove from incomplete list.
        incompleteList.remove(bestV)
        # Is the path through bestV to any uncompleted vertices better than
        # what we know so far?  If so, update that vertex pathcost and parent.
        for vertex in incompleteList:
            edgeCost = adjMatrix[bestV.index][vertex.index]
            # If there is an edge from bestV to the vertex,
            if edgeCost != 0:
                # and if the path through bestV is an improvement,
                if bestV.pathCost + edgeCost < vertex.pathCost:
                    # update the path cost and parent for the vertex.
                    vertex.pathCost = bestV.pathCost + edgeCost
                    vertex.pathParent = bestV
          
    printResult(answer)

def printResult(answer):
    for node in answer:
        #print(f"{node.label} through {node.pathParent.label} ")
        print(node.label+" through "+node.pathParent.label+" with cost",
              node.pathCost)

# Get input from the user and set that to the goal vertex
# Input has to be in the possible answers list
def userInput():
  possibleAns = ["A", "B", "C", "D", "E"]
  print("Possible choices: A, B, C, D, E")
  input1 = str(input("Which vertex to search from: ").strip().upper())
  input2 = str(input("Which vertex to search to: ").strip().upper())
  if input1 not in possibleAns:
    print(f"{input1} is not a valid input. Please try again")
    if input2 not in possibleAns:
        print(f"{input2} is not a valid input. Please try again")
        userInput()
  else:
    main(input1, input2)

userInput()
